#传入参数
param([string]$dbName ,[string]$ip,[string]$sqlFilePath,[string]$account,[string]$password)
#$dbName = "TestDemo"
#$ip = "10.129.6.6"
#$sqlFilePath = "c:\sql" 

#导入sqlps模块
  #  Import-Module sqlps -DisableNameChecking 

#检查sql server 管理单元是否存在，如果不存在就添加
try
{
	if ((get-PSSnapin sqlserverprovidersnapin100 ) -eq $null)
	{
		Add-PSSnapin sqlserverprovidersnapin100 |Out-Null
	}
	if ((get-PSSnapin sqlservercmdletsnapin100 ) -eq $null)
	{
		Add-PSSnapin sqlservercmdletsnapin100 |Out-Null
	}
}
catch
{
	
}

$SqlFileList = $dbName+"_sqlFileList.txt"
$checkFilePath = Join-Path -path $sqlFilePath -ChildPath $SqlFileList

#检测目标文件夹下是否有记录list的文本,如果没有创建并将sql脚本路径写入进去
if((Test-Path -Path $checkFilePath) -eq $false )
{
    New-Item -Path $checkFilePath -ItemType file |Out-Null 
    Get-ChildItem -Path $sqlFilePath -filter "*.sql" |ForEach-Object{
    Add-Content -Path  $checkFilePath -Value $_.fullname
    }
}

#检测目标文件件下是否有记录sql执行状态的log文件
$logFilePath = Join-Path -Path $sqlFilePath -ChildPath "sqlExecuteStatus.log"
if((Test-Path -Path $logFilePath) -eq $false)
{
	New-Item -Path $logFilePath -ItemType file |Out-Null 
}

#判断list文本是否有内容,如果有就直接执行
#| where { !([string]::IsNullOrWhiteSpace($_))}
#if((Get-Content -Path $checkFilePath | Where-Object{![System.String]::IsNullOrEmpty($_) -and ![System.String]::IsNullOrEmpty($_.Trim())}).count -gt 0)
[array]$aa = Get-Content -Path $checkFilePath | Where-Object{![System.String]::IsNullOrEmpty($_) -and ![System.String]::IsNullOrEmpty($_.Trim())}
if($aa.count -gt 0)
{
    $sqlList = Get-Content -Path $checkFilePath 
    $sqlList |ForEach-Object{
		$getDate = (Get-Date -Format "yyyy-MM-dd HH:mm:ss").tostring()
        $sqlFile = $_
        try
        {
            #Write-Host "Begin Execute SQL: "$sqlFile -BackgroundColor Green
            Invoke-Sqlcmd -ServerInstance $ip -Username $account -Password $password -Database $dbName -QueryTimeout 60 -InputFile $sqlFile  -ErrorAction Stop -OutputSqlErrors $true 
            $lineNumber = (Get-Content -Path $checkFilePath | Select-String -SimpleMatch $_).LineNumber
            $tempResult = Get-Content -Path $checkFilePath |select -Skip $lineNumber 
            #执行以后将本次循环的脚本从list中删除
            Set-Content -Path $checkFilePath -Value $tempResult
            $result = "[time]$getDate...[DB]...$dbname...[file]...$sqlFile...[status]...done"
	    	Add-Content -Path $logFilePath -Value $result -Encoding UTF8
            Write-Output $result
        }
        catch
        {
            $result = "[time]$getDate...[DB]...$dbname...[file]...$sqlFile...[status]...error:$_"
	    	Add-Content -Path $logFilePath -Value $result -Encoding UTF8
            Write-Output $result
            break
        }
    }
}
else
{
	$getDate = (Get-Date -Format "yyyy-MM-dd HH:mm:ss").tostring()
    Write-Output "No SqlFile Need to Execute"
	Add-Content -Path $logFilePath -Value "[time]...$getDate...No SqlFile Need to Execute" -Encoding UTF8
}











