# Vast.ai Documentation – Affordable GPU Cloud Marketplace

## Docs

- [create api-key](https://docs.vast.ai/api-reference/accounts/create-api-key.md): Creates a new API key with specified permissions for the authenticated user.

CLI Usage: `vastai create api-key --name <name> --permission_file <permissions_file> [--key_params <params>]`
- [create env-var](https://docs.vast.ai/api-reference/accounts/create-env-var.md): Creates a new encrypted environment variable for the authenticated user.
Keys are automatically converted to uppercase. Values are encrypted before storage.
There is a limit on the total number of environment variables per user.

CLI Usage: `vastai create env-var <key> <value>`
- [create ssh-key](https://docs.vast.ai/api-reference/accounts/create-ssh-key.md): Creates a new SSH key and associates it with your account.
The key will be automatically added to all your current instances.

CLI Usage: `vastai create ssh-key <ssh_key>`
- [create subaccount](https://docs.vast.ai/api-reference/accounts/create-subaccount.md): Creates either a standalone user account or a subaccount under a parent account. Subaccounts can be restricted to host-only functionality.

CLI Usage: `vastai create subaccount --email <email> --username <username> --password <password> [--type host]`
- [delete api key](https://docs.vast.ai/api-reference/accounts/delete-api-key.md): Deletes an existing API key belonging to the authenticated user.
The API key is soft-deleted by setting a deleted_at timestamp.

CLI Usage: `vastai delete api-key <id>`
- [delete env var](https://docs.vast.ai/api-reference/accounts/delete-env-var.md): Deletes an environment variable associated with the authenticated user.
The variable must exist and belong to the requesting user.

CLI Usage: `vastai delete env-var <name>`
- [delete ssh key](https://docs.vast.ai/api-reference/accounts/delete-ssh-key.md): Removes an SSH key from the authenticated user's account

CLI Usage: `vastai delete ssh-key <id>`
- [set user](https://docs.vast.ai/api-reference/accounts/set-user.md): Updates the user data for the authenticated user.

CLI Usage: `vastai set user --file <file_path>`
- [show api keys](https://docs.vast.ai/api-reference/accounts/show-api-keys.md): Retrieves all API keys associated with the authenticated user.

CLI Usage: `vastai show api-keys`
- [show connections](https://docs.vast.ai/api-reference/accounts/show-connections.md): Retrieves the list of cloud connections associated with the authenticated user.

CLI Usage: `vastai show connections`
- [show env vars](https://docs.vast.ai/api-reference/accounts/show-env-vars.md): Retrieve a list of environment variables (secrets) for the authenticated user.

CLI Usage: `vastai show env-vars [-s]`
- [show ipaddrs](https://docs.vast.ai/api-reference/accounts/show-ipaddrs.md): This endpoint retrieves the history of IP address accesses for the authenticated user.

CLI Usage: `vastai show ipaddrs`
- [show ssh keys](https://docs.vast.ai/api-reference/accounts/show-ssh-keys.md): Retrieve a list of SSH keys associated with the authenticated user's account.

CLI Usage: `vastai show ssh-keys`
- [show subaccounts](https://docs.vast.ai/api-reference/accounts/show-subaccounts.md): Retrieve a list of subaccounts associated with the authenticated user's account.

CLI Usage: `vastai show subaccounts`
- [show team role](https://docs.vast.ai/api-reference/accounts/show-team-role.md): Retrieve details of a specific team role by its name.

CLI Usage: `vastai show team-role <name>`
- [show user](https://docs.vast.ai/api-reference/accounts/show-user.md): Retrieve information about the current authenticated user, excluding the API key.

CLI Usage: `vastai show user`
- [transfer credit](https://docs.vast.ai/api-reference/accounts/transfer-credit.md): Transfers specified amount of credits from the authenticated user's account to another user's account.

The recipient can be specified by either email address or user ID.

CLI Usage: `vastai transfer credit <recipient_email> <amount>`
- [update env var](https://docs.vast.ai/api-reference/accounts/update-env-var.md): Updates the value of an existing environment variable for the authenticated user.

CLI Usage: `vastai update env-var <key> <value>`
- [update ssh key](https://docs.vast.ai/api-reference/accounts/update-ssh-key.md): Updates the specified SSH key with the provided value.

CLI Usage: `vastai update ssh-key <id> <ssh_key>`
- [search invoices](https://docs.vast.ai/api-reference/billing/search-invoices.md): This endpoint allows users to search and retrieve invoices based on specified filters.

CLI Usage: `vastai search invoices`
- [show deposit](https://docs.vast.ai/api-reference/billing/show-deposit.md): Retrieves the deposit details for a specified instance.

CLI Usage: `vastai show deposit <id>`
- [show earnings](https://docs.vast.ai/api-reference/billing/show-earnings.md): Retrieves the earnings history for a specified time range and optionally per machine.

CLI Usage: `vastai show earnings [options]`
- [show invoices](https://docs.vast.ai/api-reference/billing/show-invoices.md): This endpoint retrieves billing history reports for the authenticated user, including charges and credits.

CLI Usage: `vastai show invoices`
- [attach ssh-key](https://docs.vast.ai/api-reference/instances/attach-ssh-key.md): Attaches an SSH key to the specified instance, allowing SSH access using the provided key.

CLI Usage: `vastai attach ssh <instance_id> <ssh_key>`
- [cancel copy](https://docs.vast.ai/api-reference/instances/cancel-copy.md): Cancel a remote copy operation specified by the destination ID (dst_id).

CLI Usage: `vastai cancel copy --dst_id <destination_id>`
- [cancel sync](https://docs.vast.ai/api-reference/instances/cancel-sync.md): Cancels an in-progress remote sync operation identified by the destination instance ID.
This operation cannot be resumed once canceled and must be restarted if needed.

CLI Usage: `vastai cancel sync --dst_id <destination_id>`
- [change bid](https://docs.vast.ai/api-reference/instances/change-bid.md): Change the current bid price of an instance to a specified price.

CLI Usage: `vastai change bid <id> --price <price>`
- [cloud copy](https://docs.vast.ai/api-reference/instances/cloud-copy.md): Starts a cloud copy operation by sending a command to the remote server. The operation can transfer data between an instance and a cloud service.

CLI Usage: `vastai cloud copy <instance_id> <src> <dst> [options]`
- [copy](https://docs.vast.ai/api-reference/instances/copy.md): Initiate a remote copy operation to transfer data from one instance to another or between an instance and the local machine.

CLI Usage: `vastai copy <src_id> <dst_id> <src_path> <dst_path>`
- [create instance](https://docs.vast.ai/api-reference/instances/create-instance.md): Creates a new instance by accepting an "ask" contract from a provider.
This is the main endpoint for launching new instances on Vast.ai.

CLI Usage: `vastai create instance <offer_id> [options]`
- [destroy instance](https://docs.vast.ai/api-reference/instances/destroy-instance.md): Destroys/deletes an instance permanently. This is irreversible and will delete all data.

CLI Usage: `vastai destroy instance <id>`
- [detach ssh-key](https://docs.vast.ai/api-reference/instances/detach-ssh-key.md): Detaches an SSH key from a specified instance, removing SSH access for that key.

CLI Usage: `vastai detach <instance_id> <ssh_key_id>`
- [execute](https://docs.vast.ai/api-reference/instances/execute.md): Executes a constrained remote command on a specified instance.
The command output can be retrieved from the returned result URL.

CLI Usage: `vastai execute <instance_id> <command>`
- [manage instance](https://docs.vast.ai/api-reference/instances/manage-instance.md): Manage instance state and labels. The operation is determined by the request body parameters.

CLI Usage:
- To stop: `vastai stop instance <id>`
- To start: `vastai start instance <id>`
- To label: `vastai label instance <id> <label>`
- [prepay instance](https://docs.vast.ai/api-reference/instances/prepay-instance.md): Deposit credits into a reserved instance to receive usage discounts.
The discount rate is calculated based on how many months of usage the prepaid amount covers. Maximum discount is typically 40%.

CLI Usage: `vastai prepay instance <id> <amount>`
- [reboot instance](https://docs.vast.ai/api-reference/instances/reboot-instance.md): Stops and starts a container without losing GPU priority. Updates container status to 'rebooting' and executes docker stop/start commands on the host machine.

CLI Usage: `vastai reboot instance <id>`
- [recycle instance](https://docs.vast.ai/api-reference/instances/recycle-instance.md): Destroys and recreates container in place (from newly pulled image) without losing GPU priority.
Updates container status to 'recycling' and executes docker stop/remove commands on the host machine.

CLI Usage: `vastai recycle instance <id>`
- [show instance](https://docs.vast.ai/api-reference/instances/show-instance.md): Retrieves the details of a specific instance for the authenticated user.
This endpoint returns detailed information including SSH connection parameters, instance state, resource utilization, template data, and pricing details.

CLI Usage: `vastai show instance [--api-key <api_key>] [--raw]`
- [show instances](https://docs.vast.ai/api-reference/instances/show-instances.md): Retrieve a list of instances for the authenticated user.

CLI Usage: `vastai show instances [options] [--api-key <api_key>] [--raw]`
- [show logs](https://docs.vast.ai/api-reference/instances/show-logs.md): Request logs from a specific instance. The logs will be uploaded to S3 and can be retrieved from a generated URL. Supports both container logs and daemon system logs.

CLI Usage: `vastai show logs <instance_id> [--tail <lines>] [--filter <grep>] [--daemon-logs]`
- [show ssh-keys](https://docs.vast.ai/api-reference/instances/show-ssh-keys.md): Retrieves the SSH keys associated with a specific instance.

CLI Usage: `vastai show ssh-keys <instance_id>`
- [API Introduction](https://docs.vast.ai/api-reference/introduction.md)
- [cancel maint](https://docs.vast.ai/api-reference/machines/cancel-maint.md): Cancel a scheduled maintenance window for a specified machine.

CLI Usage: `vastai cancel maint <machine_id>`
- [cleanup machine](https://docs.vast.ai/api-reference/machines/cleanup-machine.md): This endpoint removes expired contracts on a specified machine, freeing up space.

CLI Usage: `vastai cleanup machine <machine_id>`
- [list machine](https://docs.vast.ai/api-reference/machines/list-machine.md): Creates or updates ask contracts for a machine to list it for rent on the vast.ai platform.
Allows setting pricing, minimum GPU requirements, end date and discount rates.

CLI Usage: `vastai list machine <machine_id> [options]`
- [remove defjob](https://docs.vast.ai/api-reference/machines/remove-defjob.md): Deletes the default job (background instances) for a specified machine.

CLI Usage: `vastai remove defjob <machine_id>`
- [schedule maint](https://docs.vast.ai/api-reference/machines/schedule-maint.md): Schedules a maintenance window for a specified machine and notifies clients.

CLI Usage: `vastai schedule maint <machine_id> --sdate <sdate> --duration <duration>`
- [set defjob](https://docs.vast.ai/api-reference/machines/set-defjob.md): Creates default jobs (background instances) for a specified machine with the given parameters.

CLI Usage: `vastai set defjob <machine_id> --price_gpu <price> --price_inetu <price> --price_inetd <price> --image <image> [--args <args>]`
- [set min-bid](https://docs.vast.ai/api-reference/machines/set-min-bid.md): Sets the minimum bid price for a specified machine.

CLI Usage: `vastai set min-bid <machine_id> --price <price>`
- [show machines](https://docs.vast.ai/api-reference/machines/show-machines.md): Fetches data for multiple machines associated with the authenticated user.

CLI Usage: `vastai show machines [--user_id <user_id>]`
- [show reports](https://docs.vast.ai/api-reference/machines/show-reports.md): Retrieves a list of the most recent reports for a given machine. Each report includes details such as the problem identified, a message describing the issue, and the timestamp when the report was created.

CLI Usage: `vastai reports <machine_id>`
- [unlist machine](https://docs.vast.ai/api-reference/machines/unlist-machine.md): Removes all 'ask' type offer contracts for a specified machine, effectively unlisting it from being available for rent.

CLI Usage: `vastai unlist machine <id>`
- [add network-disk](https://docs.vast.ai/api-reference/network-volumes/add-network-disk.md): Adds a network disk to be used to create network volume offers, or adds machines to an existing network disk.

CLI Usage: `vastai add network_disk <machine_id>... <mount_point> [options]`
- [create network-volume](https://docs.vast.ai/api-reference/network-volumes/create-network-volume.md): Creates a network volume from an offer.

CLI Usage: `vastai create network-volume <offer_id> <size> [--name <name>]`
- [list network-volume](https://docs.vast.ai/api-reference/network-volumes/list-network-volume.md): Lists a network disk for rent as network volumes, or updates an existing listing with a new price/size/end date/discount.

CLI Usage: `vastai list network-volume <disk_id> [options]`
- [search network volumes](https://docs.vast.ai/api-reference/network-volumes/search-network-volumes.md): Search for available network volume offers with advanced filtering and sorting.

CLI Usage: `vastai search network-volumes <query> [--order <field>]`
- [unlist network-volume](https://docs.vast.ai/api-reference/network-volumes/unlist-network-volume.md): Unlists a network volume for rent.

CLI Usage: `vastai unlist volume <offer_id>`
- [search benchmarks](https://docs.vast.ai/api-reference/search/search-benchmarks.md): Retrieve benchmark data based on search parameters.

CLI Usage: `vastai search benchmarks`
- [search offers](https://docs.vast.ai/api-reference/search/search-offers.md): Search for available GPU machine offers with advanced filtering and sorting.

Each filter parameter (such as `verified`, `gpu_name`, `num_gpus`, etc.) should be an object specifying the operator and value you want to match.

**Filter operators:**

| Operator | Meaning                | Example                        |
|:---------|:-----------------------|:-------------------------------|
| `eq`     | Equal to               | `{ "eq": true }`               |
| `neq`    | Not equal to           | `{ "neq": false }`             |
| `gt`     | Greater than           | `{ "gt": 0.99 }`               |
| `lt`     | Less than              | `{ "lt": 10000 }`              |
| `gte`    | Greater than or equal  | `{ "gte": 4 }`                 |
| `lte`    | Less than or equal     | `{ "lte": 8 }`                 |
| `in`     | Value is in a list     | `{ "in": ["RTX_3090", "RTX_4090"] }` |
| `nin`    | Value is not in a list | `{ "nin": ["TW", "SE"] }`      |

Default filters: verified=true, rentable=true, rented=false (unless --no-default is used)

CLI Usage: `vastai search offers 'reliability > 0.99 num_gpus>=4' --order=dph_total`
- [search templates](https://docs.vast.ai/api-reference/search/search-templates.md): Searches for templates based on query parameters and retrieves matching templates.

CLI Usage: `vastai search templates`
- [create endpoint](https://docs.vast.ai/api-reference/serverless/create-endpoint.md): This endpoint creates a new job processing endpoint with specified parameters.

CLI Usage: `vastai create endpoint [options]`
- [create workergroup](https://docs.vast.ai/api-reference/serverless/create-workergroup.md): Creates a new workergroup configuration that manages worker instances for a serverless endpoint.

CLI Usage: `vastai create workergroup --template_hash <hash> --endpoint_name <name> [options]`
- [delete endpoint](https://docs.vast.ai/api-reference/serverless/delete-endpoint.md): Deletes an endpoint group by ID. Associated workergroups will also be deleted.

CLI Usage: `vastai delete endpoint <id>`
- [delete workergroup](https://docs.vast.ai/api-reference/serverless/delete-workergroup.md): Deletes an existing workergroup.

CLI Usage: `vastai delete workergroup <id>`
- [get endpoint logs](https://docs.vast.ai/api-reference/serverless/get-endpoint-logs.md): Retrieves logs for a specific endpoint by name.

CLI Usage: `vastai get endpoint logs <endpoint_name> [--tail <num_lines>]`
- [get endpoint workers](https://docs.vast.ai/api-reference/serverless/get-endpoint-workers.md): Retrieves the current list and status of workers for a specific endpoint.
Useful for monitoring, debugging connectivity issues, and understanding resource usage.

CLI Usage: `vastai get endpoint workers <id>`
- [get workergroup logs](https://docs.vast.ai/api-reference/serverless/get-workergroup-logs.md): Retrieves logs for a specific workergroup by ID.

CLI Usage: `vastai get workergroup logs <id> [--tail <num_lines>]`
- [get workergroup workers](https://docs.vast.ai/api-reference/serverless/get-workergroup-workers.md): Retrieves the current list and status of workers for a specific workergroup.
Useful for monitoring, debugging connectivity issues, and understanding resource usage within a workergroup.

CLI Usage: `vastai get workergroup workers <id>`
- [route](https://docs.vast.ai/api-reference/serverless/route.md): Calls on the serverless engine to retrieve a GPU instance address within your endpoint for processing a request.
The engine will return either a ready worker URL or status information if no workers are available.

CLI Usage: `vastai route <endpoint> <cost>`
- [show endpoints](https://docs.vast.ai/api-reference/serverless/show-endpoints.md): Retrieve a list of endpoint jobs for the authenticated user.

CLI Usage: `vastai show endpoints`
- [show workergroup](https://docs.vast.ai/api-reference/serverless/show-workergroup.md): Retrieves the list of workergroups associated with the authenticated user.

CLI Usage: `vastai show workergroups`
- [update workergroup](https://docs.vast.ai/api-reference/serverless/update-workergroup.md): Updates the properties of an existing workergroup based on the provided parameters.

CLI Usage: `vastai update workergroup <id> [options]`
- [create team](https://docs.vast.ai/api-reference/team/create-team.md): Creates a new [team](https://docs.vast.ai/documentation/teams/teams-overview) with given name and following default roles:
- **Owner**: Full access to all team resources, settings, and member management. The team owner is the user who creates the team.
- **Manager**: All permissions of owner except team deletion.
- **Member**: Can view, create, and interact with instances, but cannot access billing, team management, autoscaler, or machines.

- The API key used to create the team becomes the team key and is used for all team operations (e.g., creating roles, deleting the team).
- You can optionally transfer credits from your personal account to the new team account using the `transfer_credit` field.

CLI Usage: `vastai create team --team_name <team_name> [--transfer_credit <amount>]`
- [create team role](https://docs.vast.ai/api-reference/team/create-team-role.md): Creates a new role within a team. Only team owners or managers with the appropriate permissions can perform this operation.

CLI Usage: `vastai create team role --name <role_name> --permissions <permissions_json>`
- [destroy team](https://docs.vast.ai/api-reference/team/destroy-team.md): Deletes a team and all associated data including API keys, rights, invitations, memberships and metadata. The team owner's master API key is converted to a normal client key.

CLI Usage: `vastai destroy team`
- [invite team member](https://docs.vast.ai/api-reference/team/invite-team-member.md): Sends an invitation email to the specified user to join the team with the given role.

CLI Usage: `vastai invite team-member --email <email> --role <role>`
- [remove team member](https://docs.vast.ai/api-reference/team/remove-team-member.md): Removes a member from the team by revoking their team-related API keys and updating membership status. Cannot remove the team owner.

CLI Usage: `vastai remove team-member <id>`
- [remove team role](https://docs.vast.ai/api-reference/team/remove-team-role.md): Removes a role from the team. Cannot remove the team owner role.

CLI Usage: `vastai remove team-role <name>`
- [show team members](https://docs.vast.ai/api-reference/team/show-team-members.md): Retrieve a list of team members associated with the authenticated user's team.

CLI Usage: `vastai show team-members`
- [show team roles](https://docs.vast.ai/api-reference/team/show-team-roles.md): Retrieve a list of all roles for a team, excluding the owner' role.

CLI Usage: `vastai show team-roles`
- [update team role](https://docs.vast.ai/api-reference/team/update-team-role.md): Update an existing team role with new name and permissions.

CLI Usage: `vastai update team-role <id> --name <new_name> --permissions <new_permissions_json>`
- [create template](https://docs.vast.ai/api-reference/templates/create-template.md): Creates a new template for launching instances. If an identical template already exists, returns the existing template instead of creating a duplicate.

CLI Usage: `vastai create template [options]`
- [delete volume](https://docs.vast.ai/api-reference/volumes/delete-volume.md): Delete a volume by its ID.

CLI Usage: `vastai delete volume <volume_id>`
- [list volumes](https://docs.vast.ai/api-reference/volumes/list-volumes.md): Retrieve information about all volumes rented by you.

CLI Usage: `vastai show volumes`
- [rent volume](https://docs.vast.ai/api-reference/volumes/rent-volume.md): Rent/create a new volume with specified parameters.

CLI Usage: `vastai create volume <id> --size <size_gb>`
- [search volumes](https://docs.vast.ai/api-reference/volumes/search-volumes.md): Search for available volumes based on specified criteria.

CLI Usage: `vastai search volumes <query> [options]`
- [unlist volume](https://docs.vast.ai/api-reference/volumes/unlist-volume.md): Remove a volume listing from the marketplace.

CLI Usage: `vastai unlist volume <volume_id>`
- [Blender Batch Rendering](https://docs.vast.ai/blender-batch-rendering.md)
- [Blender in the Cloud](https://docs.vast.ai/blender-in-the-cloud.md)
- [Commands](https://docs.vast.ai/cli/commands.md)
- [Overview & quickstart](https://docs.vast.ai/cli/get-started.md)
- [Permissions-and-authorization](https://docs.vast.ai/cli/installation.md)
- [CUDA](https://docs.vast.ai/cuda.md)
- [Disco Diffusion](https://docs.vast.ai/disco-diffusion.md)
- [Welcome to Vast.ai](https://docs.vast.ai/documentation/get-started/index.md): Step-by-step Vast.ai developer documentation with examples, guides, and API references.
- [QuickStart](https://docs.vast.ai/documentation/get-started/quickstart.md)
- [Clusters](https://docs.vast.ai/documentation/host/clusters.md)
- [Datacenter Status](https://docs.vast.ai/documentation/host/datacenter-status.md)
- [Earning](https://docs.vast.ai/documentation/host/earning.md)
- [Tax Guide for Hosts](https://docs.vast.ai/documentation/host/guide-to-taxes.md)
- [Hosting Overview](https://docs.vast.ai/documentation/host/hosting-overview.md)
- [Host Payouts](https://docs.vast.ai/documentation/host/payment.md)
- [Verification Stages](https://docs.vast.ai/documentation/host/verification-stages.md)
- [Finding & Renting Instances](https://docs.vast.ai/documentation/instances/choosing/find-and-rent.md): Find and rent GPU instances on Vast.ai. Learn how to search, filter, understand offer cards, and configure your instance.
- [Instance Types](https://docs.vast.ai/documentation/instances/choosing/instance-types.md): Understand Vast.ai instance types - On-demand, Reserved, and Interruptible. Learn how each type works, their differences, and when to use each.
- [Overview](https://docs.vast.ai/documentation/instances/choosing/overview.md): Learn the complete process of selecting and renting a GPU instance on Vast.ai, from choosing templates to configuring and launching.
- [Reserved Instances](https://docs.vast.ai/documentation/instances/choosing/reserved-instances.md): Save up to 50% on GPU costs by pre-paying for reserved instances. Learn how to convert on-demand instances to reserved pricing.
- [Choosing a Template](https://docs.vast.ai/documentation/instances/choosing/templates.md): Select the right template for your Vast.ai instance. Templates define your Docker image, launch mode, and initialization settings.
- [Instance Portal](https://docs.vast.ai/documentation/instances/connect/instance-portal.md)
- [Jupyter](https://docs.vast.ai/documentation/instances/connect/jupyter.md): Run Jupyter on Vast.ai with proxy or direct HTTPS. Learn setup, TLS certificate installation, and secure connections for smooth AI/ML development.
- [Networking & Ports](https://docs.vast.ai/documentation/instances/connect/networking.md): Understand how Vast.ai handles networking, port mapping, and environment variables for Docker instances.
- [Overview](https://docs.vast.ai/documentation/instances/connect/overview.md): Learn about Vast.ai connection methods—SSH, Jupyter, and Entrypoint—and how each controls instance access and workflow.
- [SSH Connection](https://docs.vast.ai/documentation/instances/connect/ssh.md): Learn how to securely connect to Vast.ai instances using SSH. Generate keys, establish connections, use port forwarding, and integrate with VS Code.
- [Windows SSH Guide](https://docs.vast.ai/documentation/instances/connect/windows-guide.md): Learn how to securely connect to Vast.ai instances using SSH on Windows. Understand the basics of SSH, how to generate and add keys, and how to use PuTTY and MobaXterm for GUI-based connections.
- [Managing Instances](https://docs.vast.ai/documentation/instances/manage-instances.md): Learn how to manage running instances - start, stop, destroy, monitor status, and handle common operational tasks.
- [Instances Overview](https://docs.vast.ai/documentation/instances/overview.md): Instances are Docker containers that give you exclusive GPU access for training, inference, and development. Pay by the second, connect via SSH or Jupyter.
- [Pricing](https://docs.vast.ai/documentation/instances/pricing.md): Understand Vast.ai's marketplace pricing model, rental types, reserved discounts, and costs for GPU instances.
- [Scheduled Cloud Backups](https://docs.vast.ai/documentation/instances/storage/cloud-backups.md): Learn how to set up and schedule automated Vast.ai cloud backups using CLI or cron. Keep your data safe with best practices and easy management.
- [Cloud Sync](https://docs.vast.ai/documentation/instances/storage/cloud-sync.md): Learn how to connect Vast.ai instances with cloud storage providers like Google Drive, S3, Backblaze, and Dropbox for secure data sync.
- [Data Movement](https://docs.vast.ai/documentation/instances/storage/data-movement.md): Learn how to move data on Vast.ai using cloud sync, instance-to-instance transfers, CLI copy, VM migration, scp, and other efficient methods.
- [Storage Types](https://docs.vast.ai/documentation/instances/storage/types.md): Understand the different storage options available on Vast.ai instances, including container storage and volumes.
- [Volumes](https://docs.vast.ai/documentation/instances/storage/volumes.md)
- [Account Settings](https://docs.vast.ai/documentation/reference/account-settings.md)
- [Billing](https://docs.vast.ai/documentation/reference/billing.md)
- [Billing Help](https://docs.vast.ai/documentation/reference/billing-help.md)
- [General FAQ](https://docs.vast.ai/documentation/reference/faq/general.md): Basic questions about the Vast.ai platform
- [FAQ Overview](https://docs.vast.ai/documentation/reference/faq/index.md): Find answers to common questions about Vast.ai
- [Instances FAQ](https://docs.vast.ai/documentation/reference/faq/instances.md): Questions about creating and managing instances
- [Jupyter & SSH FAQ](https://docs.vast.ai/documentation/reference/faq/jupyter-ssh.md): Connecting to instances via Jupyter and SSH
- [Networking](https://docs.vast.ai/documentation/reference/faq/networking.md)
- [Rental Types FAQ](https://docs.vast.ai/documentation/reference/faq/rental-types.md): Understanding on-demand vs interruptible instances
- [Security FAQ](https://docs.vast.ai/documentation/reference/faq/security.md): Data protection and platform security
- [Technical FAQ](https://docs.vast.ai/documentation/reference/faq/technical.md): Docker configuration, performance, and advanced topics
- [Keys](https://docs.vast.ai/documentation/reference/keys.md)
- [Referral Program](https://docs.vast.ai/documentation/reference/referral-program.md)
- [Troubleshooting](https://docs.vast.ai/documentation/reference/troubleshooting.md)
- [Architecture](https://docs.vast.ai/documentation/serverless/architecture.md): Understand the architecture of Vast.ai Serverless, including the Serverless System, GPU Instances, and User (Client Application). Learn how the system works, how to use the routing process, and how to create Worker Groups.
- [Comfy UI](https://docs.vast.ai/documentation/serverless/comfy-ui.md): Learn how to use Comfy UI with Vast.ai Serverless for image generation workflows.
- [Create Endpoints and Workergroups](https://docs.vast.ai/documentation/serverless/create-endpoints-and-workergroups.md): Learn how to create endpoints and workergroups in Vast.ai Serverless. Understand the inputs, outputs, and examples for creating endpoints and workergroups.
- [Creating New PyWorkers](https://docs.vast.ai/documentation/serverless/creating-new-pyworkers.md): Learn how to create a new PyWorker for Vast.ai Serverless. Understand the structure of a PyWorker, the required files, and how to implement the server.py module.
- [Debugging](https://docs.vast.ai/documentation/serverless/debugging.md): Learn how to debug issues with Vast.ai Serverless. Understand the worker errors, increasing and decreasing load, and how to check the instance logs.
- [Getting Started With Serverless](https://docs.vast.ai/documentation/serverless/getting-started-with-serverless.md): Learn how to get started with Vast.ai Serverless. Understand the prerequisites, setup process, and how to use the serverless engine.
- [Serverless Overview](https://docs.vast.ai/documentation/serverless/index.md): Learn how to use Vast.ai's Serverless system to automate the provisioning of GPU workers to match the dynamic computational needs of your workloads.
- [Inside a Serverless GPU](https://docs.vast.ai/documentation/serverless/inside-a-serverless-gpu.md): Learn about the components of a Serverless GPU instance - the core ML model, model server code, and PyWorker server code.
- [Logs](https://docs.vast.ai/documentation/serverless/logs.md): Learn how to fetch and analyze logs from Vast.ai Serverless endpoints and worker groups. Understand the log levels, how to use cURL to fetch logs, and how to interpret the logs for debugging and performance monitoring.
- [Overview](https://docs.vast.ai/documentation/serverless/overview.md): Learn about Vast.ai's Serverless system - the Vast PyWorker, integration with model instances, and creating custom backends.
- [Performance Testing](https://docs.vast.ai/documentation/serverless/performance-testing.md): Learn about the performance testing process in Vast.ai Serverless. Understand how the test measures LLM and image generation capabilities, how it translates pixel generation to tokens, and how it normalizes performance across different GPUs.
- [Pricing](https://docs.vast.ai/documentation/serverless/pricing.md): Learn how Vast.ai Serverless pricing works - GPU recruitment, endpoint suspension, and stopping.
- [Route](https://docs.vast.ai/documentation/serverless/route.md): Learn how to use the /route/ endpoint to retrieve a GPU instance address within your Endpoint. Understand the inputs, outputs, and examples for using the endpoint.
- [Serverless Parameters](https://docs.vast.ai/documentation/serverless/serverless-parameters.md): Learn about the parameters that can be configured for Vast.ai Serverless endpoints and worker groups.
- [Text Generation Inference (TGI)](https://docs.vast.ai/documentation/serverless/text-generation-inference-tgi.md): Learn how to use Text Generation Inference (TGI) with Vast.ai Serverless for text generation models.
- [vLLM](https://docs.vast.ai/documentation/serverless/vllm.md): Learn how to use vLLM with Vast.ai Serverless for large language model inference.
- [Worker List](https://docs.vast.ai/documentation/serverless/worker-list.md): Learn how to use the /get_endpoint_workers/ and /get_autogroup_workers/ endpoints to retrieve a list of GPU instances under an Endpoint and Worker Group. Understand the inputs, outputs, and examples for using the endpoints.
- [Legacy Teams](https://docs.vast.ai/documentation/teams/legacy-teams.md)
- [Managing Your Team](https://docs.vast.ai/documentation/teams/managing-teams.md)
- [Teams Overview](https://docs.vast.ai/documentation/teams/teams-overview.md)
- [Teams Quickstart](https://docs.vast.ai/documentation/teams/teams-quickstart.md)
- [Teams Roles](https://docs.vast.ai/documentation/teams/teams-roles.md)
- [Advanced Setup](https://docs.vast.ai/documentation/templates/advanced-setup.md)
- [Creating Templates](https://docs.vast.ai/documentation/templates/creating-templates.md)
- [Creating Templates for GROBID](https://docs.vast.ai/documentation/templates/examples/grobid.md)
- [Templates](https://docs.vast.ai/documentation/templates/introduction.md)
- [Managing Templates](https://docs.vast.ai/documentation/templates/managing-templates.md)
- [Quick Start](https://docs.vast.ai/documentation/templates/quickstart.md)
- [Template Settings](https://docs.vast.ai/documentation/templates/template-settings.md)
- [Google Colab](https://docs.vast.ai/google-colab.md)
- [Huggingface TGI with LLama3](https://docs.vast.ai/huggingface-tgi-with-llama3.md)
- [Image Generation](https://docs.vast.ai/image-generation.md)
- [Infinity Embeddings](https://docs.vast.ai/infinity-embeddings.md)
- [Langflow + Ollama](https://docs.vast.ai/langflow-ollama.md)
- [Linux Virtual Desktop](https://docs.vast.ai/linux-virtual-desktop.md)
- [Linux Virtual Machines](https://docs.vast.ai/linux-virtual-machines.md)
- [Mining on Bittensor](https://docs.vast.ai/mining-on-bittensor.md)
- [Multi-Node training using Torch + NCCL](https://docs.vast.ai/multi-node-training-using-torch-nccl.md)
- [Ollama + Webui](https://docs.vast.ai/ollama-webui.md)
- [Oobabooga (LLM webui)](https://docs.vast.ai/oobabooga-llm-webui.md)
- [PyTorch](https://docs.vast.ai/pytorch.md)
- [Quantized GGUF models (cloned)](https://docs.vast.ai/quantized-gguf-models-cloned.md)
- [RTX 5 Series](https://docs.vast.ai/rtx-5-series.md): Optimize your GPU experience with our comprehensive guide on RTX 5 Series GPUs (5090/5080/5070) and CUDA 12.8 compatibility. Learn how to rent an RTX 5090 on Vast.ai, select the right templates, and customize your storage while ensuring optimal performance.
- [Python SDK Usage](https://docs.vast.ai/sdk/python/quickstart.md)
- [Stable Diffusion](https://docs.vast.ai/stable-diffusion.md)
- [TTS with Nari Labs Dia](https://docs.vast.ai/tts-with-nari-labs-dia.md)
- [Video Generation](https://docs.vast.ai/video-generation.md)
- [vLLM (LLM inference and serving)](https://docs.vast.ai/vllm-llm-inference-and-serving.md)
- [VMs](https://docs.vast.ai/vms.md)
- [Whisper ASR Guide](https://docs.vast.ai/whisper-asr-guide.md)
