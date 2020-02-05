[CmdletBinding()] Param(
    $pythonVersion = "3.8.1",
    $pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion.exe",
    $pythonDownloadPath = 'C:\Tools\python-$pythonVersion.exe',
    $pythonInstallDir = "C:\Tools\Python$pythonVersion"
)

(New-Object Net.WebClient).DownloadFile($pythonUrl, $pythonDownloadPath)
& $pythonDownloadPath /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_test=0 TargetDir=$pythonInstallDir
if ($LASTEXITCODE -ne 0) {
    throw "The python installer at '$pythonDownloadPath' exited with error code '$LASTEXITCODE'"
}
# Set the PATH environment variable for the entire machine (that is, for all users) to include the Python install dir
[Environment]::SetEnvironmentVariable("PATH", "${env:path};${pythonInstallDir}", "Machine")
# SIG # Begin signature block
# MIIFdgYJKoZIhvcNAQcCoIIFZzCCBWMCAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQU/RW/65vkJHPiy//HBpulh6g3
# ny+gggMOMIIDCjCCAfKgAwIBAgIQLANDVh0MC6lDXHZgtnSMWTANBgkqhkiG9w0B
# AQUFADAdMRswGQYDVQQDDBJMb2NhbCBDb2RlIFNpZ25pbmcwHhcNMjAwMjA1MDcz
# NTIyWhcNMjEwMjA1MDc1NTIyWjAdMRswGQYDVQQDDBJMb2NhbCBDb2RlIFNpZ25p
# bmcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC9wrwe2sMAF4c0HTla
# I6nsbzyeJk+XGLyCIe/ZfwH4HgP3hPTQSNoNPU9TLqIXXLvY8wDBoEuSwCyHNqLj
# wMeT3U1gV0+5j7gVa2Ca8tsVxMhWjY9qRcIuQbo+yUWvRPTzIJ14PeIneHkWxlP6
# IRnYfta1jUSyLnTcXdPimvtxrzFqZHS8EJSmcAARzOHnyILM4rI87LOGORXdQTlI
# RPrMK+GFheTEa4FXQro34vBHTSrLW2cnIwF3FJPtwQV+QBJHuP0tYOWr8D/nVdN9
# jPD5o6tS9KG1WZyPYZIXdo3fZeofO318pRTlWupFccS8WzIU5+jaMd7kKIh9rP64
# iVZZAgMBAAGjRjBEMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcD
# AzAdBgNVHQ4EFgQUbn4G2uwepFIr/+iDFMdsww6v1SQwDQYJKoZIhvcNAQEFBQAD
# ggEBALOQq9mq/rle3Ue8VF6z3UXjSJuJTSCb/myjOCv7PzF3hQDRvtKyZy0yN/Z2
# kCGMEnsMBSk+qzVXEymJk4m0Gfc7JUgCcm+4vv7iGSC94Knz9lUrgkeC/RCgl+eI
# n8RLciSZBeihu7apMkyZWbiI47HbwHn9LkwDaQ8fRDvjKcWW27R1Cg0hkEfQ8Oze
# 7Pli7MCfbyzCXGCwV6/h6MitSpWy8lm5WYD65nDk8EhwOjAM3xoP0lFcOmVcnjj9
# I5U6CEfQpw0vknDZnzeKdvhi/WEY05Cn75zN6Xj96EtQloe48x9Cu/Qn7NRKNQ2T
# wCvLsrZaTvLuhSU+QqKJzHLqlj0xggHSMIIBzgIBATAxMB0xGzAZBgNVBAMMEkxv
# Y2FsIENvZGUgU2lnbmluZwIQLANDVh0MC6lDXHZgtnSMWTAJBgUrDgMCGgUAoHgw
# GAYKKwYBBAGCNwIBDDEKMAigAoAAoQKAADAZBgkqhkiG9w0BCQMxDAYKKwYBBAGC
# NwIBBDAcBgorBgEEAYI3AgELMQ4wDAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQx
# FgQU6CWbO7OEJ1wWM3BWrppkA6WKkcAwDQYJKoZIhvcNAQEBBQAEggEAenHjzmIX
# s4HDNSmdxhPtj4t8Sj+Na6jgjL7wwlfF7DNMc7vj9awTCKaj1bi+uPBqpDjZC481
# RufPS6r4VTLwFwUEnsLdbvNShUlYsTQJ4fB6UAnfZ3L25vQ3bhiaww6N38bd6T/P
# 0CqxOPTxgPReKuIc4Y1Ph+w+ZVq1ugQ9SA8zPlEnANoOstEyZs2B+hj0trdPezvU
# BOegjWCG5dNpc8++IXcAqeHFVU08QyxIdHoR2EQTtOKHB3Jj7ZCXbM79yDPAz8ZB
# hU8folMMJO7L2O4q6/wUZ37jZyKkRktom+f0Jn2JyRwWB0h03LujHSw4AfQR7G8U
# l69r5dCK4jXmOQ==
# SIG # End signature block
