# Step-by-Step Guide to Set Up ELK Stack with Filebeat

## Requirements
Ensure the following software is installed on your system:

1. **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
2. **Docker Desktop** (for Windows users) - [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
3. **Docker Compose** - [Install Docker Compose](https://docs.docker.com/compose/install/)
4. **VirtualBox** - [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
5. **Vagrant** - [Install Vagrant](https://developer.hashicorp.com/vagrant/downloads)
   
Alternatively, you can use a standalone VM instead of VirtualBox + Vagrant.

---

## Setup ELK Stack

1. Clone the GitHub repository:
   ```bash
   git clone https://github.com/envyst/test-inotech.git
   ```

2. Navigate to the project directory:
   ```bash
   cd section4-security-task
   ```

3. Start the ELK stack using Docker Compose:
   ```bash
   docker compose up -d
   ```

---

## Setup Linux VM

### Option I: VirtualBox + Vagrant

1. Run Vagrant to set up the virtual machine and install Filebeat:
   ```bash
   vagrant up
   ```

---

### Option II: Standalone VM

1. Install Filebeat on the VM:

   ```bash
   # Update system and install dependencies
   apt-get update
   apt-get install -y apt-transport-https wget

   # Install Filebeat
   wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
   echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list
   apt-get update
   apt-get install -y filebeat
   ```

2. Configure Filebeat by editing `/etc/filebeat/filebeat.yml`:

   ```yaml
   filebeat.inputs:
   - type: filestream
     id: my-filestream-1
     enabled: true
     paths:
       - /var/log/command.log
     fields:
       log_type: command
     fields_under_root: false

   - type: filestream
     id: my-filestream-2
     enabled: true
     paths:
       - /var/log/auth.log
     fields:
       log_type: auth
     fields_under_root: false
     processors:
       - dissect:
           tokenizer: "%{timestamp} %{hostname} %{process}[%{pid}]: %{message}"
           field: "message"
           target_prefix: "auth"
           ignore_failure: true
       - drop_fields:
           fields: ["host", "agent", "ecs"]

   output.logstash:
     hosts: ["192.168.56.1:5044"] # Replace with Logstash IP, Here I am using Docker Desktop Host IP
   ```

3. Configure `/etc/bash.bashrc` to stream terminal commands to a log file:
   ```bash
   export PROMPT_COMMAND='echo "$(date +"%Y-%m-%d %H:%M:%S") $(whoami) $(history 1)" >> /var/log/command.log'
   ```

4. Test and enable Filebeat:
   ```bash
   filebeat test config # Ensure the configuration is OK
   filebeat modules enable system
   systemctl enable filebeat
   systemctl start filebeat # Or use systemctl restart filebeat
   ```

5. Test Filebeat:
   - Execute some commands in the terminal.
   ```bash
   whoami
   ls
   mkdir test
   cd test
   touch somegrass
   ssh invaliduser@localhost
   #etc
   ```

6. Check the data view in Kibana to verify logs.

---

Enjoy your ELK stack setup with Filebeat!
