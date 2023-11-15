# enceladus
OracleHealthAPI Beta Software

### Pre-Development

apt-get update \
apt-get install -y git python3 python3-pip lvm2 apt-transport-https ca-certificates curl gnupg \
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker.gpg \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \
sudo apt update \
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin \
sudo usermod -aG docker devops \
cd /usr/bin \
ln -s python3 python \
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED \
pip install fhir.resources requests \
pip3 install mysql-connector-python \
 
### Reference Pages

https://docs.healtheintent.com/#introduction \
https://docs.healtheintent.com/#getting-started \
https://fhir.cerner.com/millennium/overview/ \
https://github.com/cerner/fhir.cerner.com \
https://fhir.cerner.com/smart/#open-source-fhir-client-libraries \
https://fhir.cerner.com/ \
https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185 \
https://hl7.org/fhir/R4/ \
 \
https://code.cerner.com/apiaccess \
https://apex.oracle.com/en/ \
 \
https://forums.oracle.com/ords/apexds/domain/open-developer-experience 

### Create MySQL Docker Storage 
echo "- - -" > /sys/class/scsi_host/host0/scan \
fdisk -l \
lsblk \
 \
pvcreate /dev/nvme1n1  \
vgcreate dockervg /dev/nvme1n1 \
lvcreate --name dblv1 -l 100%FREE dockervg \
mkfs.ext4 /dev/dockervg/dblv1 \
mkdir /opt/apps/enceladusdb \
mount /dev/dockervg/dblv1 /opt/apps/enceladusdb \
echo "/dev/dockervg/dblv1 /opt/apps/enceladusdb ext4 defaults 0 0" >> /etc/fstab

