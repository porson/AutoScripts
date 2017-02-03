#�������
param([string]$dbName ,[string]$ip,[string]$sqlFilePath,[string]$account,[string]$password)
#$dbName = "TestDemo"
#$ip = "10.129.6.6"
#$sqlFilePath = "c:\sql" 

#����sqlpsģ��
  #  Import-Module sqlps -DisableNameChecking 

#���sql server ����Ԫ�Ƿ���ڣ���������ھ����
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

#���Ŀ���ļ������Ƿ��м�¼list���ı�,���û�д�������sql�ű�·��д���ȥ
if((Test-Path -Path $checkFilePath) -eq $false )
{
    New-Item -Path $checkFilePath -ItemType file |Out-Null 
    Get-ChildItem -Path $sqlFilePath -filter "*.sql" |ForEach-Object{
    Add-Content -Path  $checkFilePath -Value $_.fullname
    }
}

#���Ŀ���ļ������Ƿ��м�¼sqlִ��״̬��log�ļ�
$logFilePath = Join-Path -Path $sqlFilePath -ChildPath "sqlExecuteStatus.log"
if((Test-Path -Path $logFilePath) -eq $false)
{
	New-Item -Path $logFilePath -ItemType file |Out-Null 
}

#�ж�list�ı��Ƿ�������,����о�ֱ��ִ��
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
            #ִ���Ժ󽫱���ѭ���Ľű���list��ɾ��
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











