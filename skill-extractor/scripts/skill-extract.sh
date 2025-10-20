#!/bin/bash
# Skill Extractor - Main Wrapper Script
#
# This script provides a simple interface for analyzing commands/agents
# and extracting reusable components into skills.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Print colored output
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

# Show usage
usage() {
    cat << EOF
Skill Extractor - Extract reusable components from Claude Code commands/agents

USAGE:
    $(basename "$0") analyze <input-file> [options]
    $(basename "$0") extract <analysis-file> --name <skill-name> [options]
    $(basename "$0") full <input-file> --name <skill-name> [options]

COMMANDS:
    analyze              Analyze a command/agent file for extractable components
    extract              Extract components using an existing analysis file
    full                 Analyze and extract in one step

OPTIONS:
    -h, --help           Show this help message
    -o, --output DIR     Output directory (default: current directory)
    -v, --verbose        Show detailed output
    -n, --name NAME      Name for the extracted skill (required for extract/full)
    --no-backup          Don't create backup of original file

EXAMPLES:
    # Analyze a command file
    $(basename "$0") analyze ~/.claude/commands/mine/agent-forge.md --verbose

    # Extract components after analysis
    $(basename "$0") extract analysis.json --name agent-creation-tools --output ./skills

    # Analyze and extract in one step
    $(basename "$0") full ~/.claude/commands/mine/novel-planner.md --name novel-planning-templates

    # Analyze an agent
    $(basename "$0") analyze ~/.claude/agents/mine/novel-chapter-writer.md

EOF
}

# Analyze command
analyze_command() {
    local input_file="$1"
    local verbose="$2"
    local output_file="analysis.json"

    if [[ ! -f "$input_file" ]]; then
        print_error "Input file not found: $input_file"
        exit 1
    fi

    print_header "Analyzing: $(basename "$input_file")"

    # Run analysis
    local analysis_cmd="python3 '$SCRIPT_DIR/analyze_command.py' '$input_file' --output '$output_file'"

    if [[ "$verbose" == "true" ]]; then
        analysis_cmd="$analysis_cmd --verbose"
    fi

    if eval "$analysis_cmd"; then
        print_success "Analysis complete"
        print_info "Results saved to: $output_file"

        # Show summary if not verbose
        if [[ "$verbose" != "true" ]]; then
            print_info "Run with --verbose for detailed output"
            print_info "Or proceed with extraction using:"
            echo "    $(basename "$0") extract $output_file --name <skill-name>"
        fi
    else
        print_error "Analysis failed"
        exit 1
    fi
}

# Extract components
extract_components() {
    local analysis_file="$1"
    local skill_name="$2"
    local output_dir="$3"

    if [[ ! -f "$analysis_file" ]]; then
        print_error "Analysis file not found: $analysis_file"
        exit 1
    fi

    if [[ -z "$skill_name" ]]; then
        print_error "Skill name is required. Use --name <skill-name>"
        exit 1
    fi

    print_header "Extracting Components"
    print_info "Skill name: $skill_name"
    print_info "Output directory: $output_dir"

    # Run extraction
    python3 "$SCRIPT_DIR/extract_components.py" "$analysis_file" \
        --name "$skill_name" \
        --output "$output_dir"
    exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        print_success "Extraction complete!"
        echo ""
        print_info "Skill created at: $output_dir/$skill_name/"
        print_info "Review the migration report: $output_dir/$skill_name/migration-report.md"
        echo ""
        print_warning "IMPORTANT: The original file was NOT modified."
        print_warning "Follow the migration report to integrate the skill."
    elif [[ $exit_code -eq 2 ]]; then
        # YAGNI check rejected extraction
        print_info "No skill was created (extraction not recommended)"
        exit 0  # Not an error, just not worth extracting
    else
        print_error "Extraction failed"
        exit 1
    fi
}

# Full process (analyze + extract)
full_process() {
    local input_file="$1"
    local skill_name="$2"
    local output_dir="$3"
    local verbose="$4"

    # Create temporary analysis file
    local temp_analysis=$(mktemp)

    print_header "Full Extraction Process"

    # Step 1: Analyze
    print_info "Step 1/2: Analyzing file..."
    if [[ ! -f "$input_file" ]]; then
        print_error "Input file not found: $input_file"
        exit 1
    fi

    local analysis_cmd="python3 '$SCRIPT_DIR/analyze_command.py' '$input_file' --output '$temp_analysis'"
    if [[ "$verbose" == "true" ]]; then
        analysis_cmd="$analysis_cmd --verbose"
    fi

    if ! eval "$analysis_cmd"; then
        print_error "Analysis failed"
        rm "$temp_analysis"
        exit 1
    fi
    print_success "Analysis complete"

    # Step 2: Extract
    print_info "Step 2/2: Extracting components..."
    python3 "$SCRIPT_DIR/extract_components.py" "$temp_analysis" \
        --name "$skill_name" \
        --output "$output_dir"
    exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        print_success "Extraction complete!"
        echo ""
        print_info "Skill created at: $output_dir/$skill_name/"
        print_info "Files created:"
        echo "  - SKILL.md"
        echo "  - migration-report.md"
        if [[ -d "$output_dir/$skill_name/scripts" ]]; then
            echo "  - scripts/"
        fi
        if [[ -d "$output_dir/$skill_name/references" ]]; then
            echo "  - references/"
        fi
        if [[ -d "$output_dir/$skill_name/assets" ]]; then
            echo "  - assets/"
        fi
        echo ""
        print_warning "IMPORTANT: Review the migration report before updating the original file."
        print_info "Migration report: $output_dir/$skill_name/migration-report.md"
    elif [[ $exit_code -eq 2 ]]; then
        # YAGNI check rejected extraction
        print_info "No skill was created (extraction not recommended)"
        rm "$temp_analysis"
        exit 0  # Not an error, just not worth extracting
    else
        print_error "Extraction failed"
        rm "$temp_analysis"
        exit 1
    fi

    # Cleanup
    rm "$temp_analysis"
}

# Main script
main() {
    local command=""
    local input_file=""
    local output_dir="."
    local skill_name=""
    local verbose="false"
    local analysis_file=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            analyze|extract|full)
                command="$1"
                shift
                ;;
            -o|--output)
                output_dir="$2"
                shift 2
                ;;
            -n|--name)
                skill_name="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose="true"
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -z "$input_file" ]] && [[ -z "$analysis_file" ]]; then
                    if [[ "$command" == "extract" ]]; then
                        analysis_file="$1"
                    else
                        input_file="$1"
                    fi
                fi
                shift
                ;;
        esac
    done

    # Validate command
    if [[ -z "$command" ]]; then
        print_error "No command specified"
        usage
        exit 1
    fi

    # Execute command
    case "$command" in
        analyze)
            if [[ -z "$input_file" ]]; then
                print_error "Input file required for analyze command"
                usage
                exit 1
            fi
            analyze_command "$input_file" "$verbose"
            ;;
        extract)
            if [[ -z "$analysis_file" ]]; then
                print_error "Analysis file required for extract command"
                usage
                exit 1
            fi
            extract_components "$analysis_file" "$skill_name" "$output_dir"
            ;;
        full)
            if [[ -z "$input_file" ]]; then
                print_error "Input file required for full command"
                usage
                exit 1
            fi
            if [[ -z "$skill_name" ]]; then
                print_error "Skill name required for full command. Use --name <skill-name>"
                usage
                exit 1
            fi
            full_process "$input_file" "$skill_name" "$output_dir" "$verbose"
            ;;
        *)
            print_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main
main "$@"
