#If error running, oper powershell as admin
#Get-ExecutionPolicy -Scope CurrentUser
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

$githuber   = "ZeroQI"
$repository = "Hama.bundle"
$branch     = "master"
$download   = "https://github.com/$githuber/$repository/archive/$branch.zip"
$zip        = $repository + ".zip"
$folder     = $repository + "-$branch"
$script     = "PowerShell Update Agent.ps1"

Write-Host
Write-Host "$githuber/$repository Github repository $branch branch - $script"
Write-Host [ ] Path: $PSScriptRoot
  
if (Test-Path README.md)
{ Write-Host [*] copying "$script" to parent folder "..\$repository.ps1"
  Copy-Item -Path "$script" -Destination "..\$repository.ps1"
  Write-Host [*] Changing running parent folder to ..
  Set-Location -Path ..
  Write-Host [*] Running ".\$repository.ps1"
  & ".\$repository.ps1"
  exit
}
else
{
  if (Test-Path $repository-old)
  { Write-Host [*] Deleting $repository-old as it was present 
    Remove-Item $repository-old -Recurse -Force
  }
  
  if (Test-Path $repository)
  { Write-Host [*] Moving  "$repository" to $repository-old
    Move-Item $repository -Destination $repository-old -Force
  }
  
  Write-Host [*] Dowloading latest release from "$download" to "$zip"
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  Invoke-WebRequest -Uri $download -Out $zip

  Write-Host [*] Extracting $zip to $folder
  Expand-Archive -Path $zip -DestinationPath .\ -Force

  Write-Host [*] Moving "$folder" to "$repository"
  Move-Item $folder -Destination $repository -Force

  Write-Host [*] Deleting $zip
  Remove-Item $zip -Force
  
  if (Test-Path .\$repository.ps1)
  { Write-Host [*] Deleting "$repository.ps1"
    Remove-Item  .\$repository.ps1 -Force
  }
    
  Write-Host
  exit
}
