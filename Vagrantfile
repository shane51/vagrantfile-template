Vagrant.require_version '>= 1.8.0'

Vagrant.configure(2) do |config|
  # always use Vagrants insecure key
  config.ssh.insert_key = false

  # Ubuntu 16.04, 64 bit
  config.vm.box         = "bento/ubuntu-16.04"
  config.vm.box         = "ubuntu/xenial64"
  config.vm.define "AppiumParallel"


  config.vm.provider :virtualbox do |v|
    v.name = 'appiumParallel_ubuntu'
   # Set memory to 4096
   # Allow I/O APIC
    v.customize ['modifyvm', :id, '--memory', '4096', '--ioapic', 'on']
    # Enable the VM's virtual USB controller & enable the virtual USB 2.0 controller
    v.customize ["modifyvm", :id, "--usb", "on", "--usbehci", "on"]
  end
end