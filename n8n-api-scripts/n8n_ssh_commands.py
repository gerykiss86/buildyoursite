"""
SSH Commands for n8n Docker Management
"""

import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv('n8n.env')

class N8NDockerManager:
    def __init__(self):
        self.ssh_host = os.getenv('SSH_HOST')
        self.ssh_user = os.getenv('SSH_USER')
        self.ssh_key = os.getenv('SSH_KEY_PATH')
        self.docker_path = os.getenv('N8N_DOCKER_PATH', '/opt/n8n')

    def run_ssh_command(self, command, show_output=True):
        """Execute SSH command on remote server"""
        ssh_cmd = f'plink -i "{self.ssh_key}" {self.ssh_user}@{self.ssh_host} "{command}"'
        try:
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
            if show_output:
                print(result.stdout)
                if result.stderr:
                    print(f"Error: {result.stderr}")
            return result.stdout, result.returncode
        except Exception as e:
            print(f"SSH Error: {e}")
            return None, 1

    def get_container_status(self):
        """Get n8n container status"""
        print("🔍 Checking n8n container status...")
        self.run_ssh_command("docker ps | grep n8n")

    def view_logs(self, lines=50):
        """View n8n container logs"""
        print(f"📋 Last {lines} lines of n8n logs:")
        self.run_ssh_command(f"docker logs --tail {lines} n8n")

    def restart_container(self):
        """Restart n8n container"""
        print("🔄 Restarting n8n container...")
        self.run_ssh_command("docker restart n8n")
        self.get_container_status()

    def stop_container(self):
        """Stop n8n container"""
        print("⏹️ Stopping n8n container...")
        self.run_ssh_command("docker stop n8n")

    def start_container(self):
        """Start n8n container"""
        print("▶️ Starting n8n container...")
        self.run_ssh_command(f"cd {self.docker_path} && docker-compose up -d")
        self.get_container_status()

    def backup_data(self):
        """Backup n8n data"""
        timestamp = subprocess.run("date +%Y%m%d_%H%M%S", shell=True, capture_output=True, text=True).stdout.strip()
        backup_file = f"n8n_backup_{timestamp}.tar.gz"
        print(f"💾 Creating backup: {backup_file}")
        self.run_ssh_command(f"docker exec n8n tar -czf /tmp/{backup_file} /home/node/.n8n")
        self.run_ssh_command(f"docker cp n8n:/tmp/{backup_file} /root/{backup_file}")
        print(f"✅ Backup saved to /root/{backup_file}")

    def update_container(self):
        """Update n8n to latest version"""
        print("🔄 Updating n8n to latest version...")
        commands = [
            "docker pull n8nio/n8n:latest",
            f"cd {self.docker_path} && docker-compose down",
            f"cd {self.docker_path} && docker-compose up -d"
        ]
        for cmd in commands:
            self.run_ssh_command(cmd)
        print("✅ Update complete")

    def check_disk_usage(self):
        """Check disk usage"""
        print("💽 Disk usage:")
        self.run_ssh_command("df -h /")
        print("\n📦 Docker volume usage:")
        self.run_ssh_command("docker system df")

    def cleanup_old_executions(self):
        """Clean up old workflow executions"""
        print("🧹 Cleaning up old executions...")
        # This would need to be done via n8n API or database directly
        print("Note: Use n8n API or database tools to clean up old executions")

    def show_environment(self):
        """Show n8n environment configuration"""
        print("⚙️ n8n Environment Configuration:")
        self.run_ssh_command(f"cat {self.docker_path}/.env")
        print("\n🐳 Docker Compose Configuration:")
        self.run_ssh_command(f"cat {self.docker_path}/docker-compose.yml")

def main():
    """Main function for interactive management"""
    manager = N8NDockerManager()

    print("=" * 60)
    print("N8N DOCKER MANAGER")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. Check container status")
        print("2. View logs")
        print("3. Restart container")
        print("4. Stop container")
        print("5. Start container")
        print("6. Backup data")
        print("7. Update n8n")
        print("8. Check disk usage")
        print("9. Show environment")
        print("0. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            manager.get_container_status()
        elif choice == "2":
            lines = input("Number of log lines (default 50): ")
            lines = int(lines) if lines else 50
            manager.view_logs(lines)
        elif choice == "3":
            confirm = input("Restart n8n container? (y/n): ")
            if confirm.lower() == 'y':
                manager.restart_container()
        elif choice == "4":
            confirm = input("Stop n8n container? (y/n): ")
            if confirm.lower() == 'y':
                manager.stop_container()
        elif choice == "5":
            manager.start_container()
        elif choice == "6":
            manager.backup_data()
        elif choice == "7":
            confirm = input("Update n8n to latest version? (y/n): ")
            if confirm.lower() == 'y':
                manager.update_container()
        elif choice == "8":
            manager.check_disk_usage()
        elif choice == "9":
            manager.show_environment()
        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()