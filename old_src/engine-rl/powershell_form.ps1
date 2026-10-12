Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Engine-RL PowerShell Form"
$form.Size = New-Object System.Drawing.Size(450, 320)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(11, 14, 20)
$form.ForeColor = [System.Drawing.Color]::FromArgb(240, 245, 255)

$lbl = New-Object System.Windows.Forms.Label
$lbl.Text = "Engine-RL PowerShell Native Form"
$lbl.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$lbl.ForeColor = [System.Drawing.Color]::FromArgb(0, 210, 255)
$lbl.Location = New-Object System.Drawing.Point(30, 40)
$lbl.AutoSize = $true
$form.Controls.Add($lbl)

$btn = New-Object System.Windows.Forms.Button
$btn.Text = "Click PowerShell Action"
$btn.Location = New-Object System.Drawing.Point(30, 100)
$btn.Size = New-Object System.Drawing.Size(370, 45)
$btn.BackColor = [System.Drawing.Color]::FromArgb(0, 180, 120)
$btn.ForeColor = [System.Drawing.Color]::White
$btn.FlatStyle = "Flat"
$btn.Add_Click({
    [System.Windows.Forms.MessageBox]::Show("Hello from Engine-RL PowerShell Form!", "Info", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
})
$form.Controls.Add($btn)

[void]$form.ShowDialog()