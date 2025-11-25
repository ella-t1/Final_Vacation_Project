# Start PostgreSQL Service

## Problem
Connection timeout in pgAdmin because **PostgreSQL service is not running**.

## Solution: Start PostgreSQL Service

### Method 1: Services App (Easiest)

1. **Press `Win + R`**
2. **Type:** `services.msc`
3. **Press Enter**
4. **Find:** "postgresql-x64-17 - PostgreSQL Server 17"
5. **Right-click** on it
6. **Click "Start"**

Wait a few seconds for it to start.

### Method 2: PowerShell (As Administrator)

```powershell
Start-Service postgresql-x64-17
```

If you get a permission error, run PowerShell as Administrator first.

### Method 3: Command Prompt (As Administrator)

```cmd
net start postgresql-x64-17
```

## Verify It's Running

After starting, check:
```powershell
Get-Service postgresql-x64-17
```

Status should show: **Running**

## Then Connect in pgAdmin

1. **Go back to pgAdmin**
2. **Right-click "PostgreSQL 17"** → **"Connect Server"**
3. **Leave password empty** (trust mode)
4. **Click Connect**

It should connect now!

## After Connecting

1. **Expand "PostgreSQL 17"**
2. **Expand "Login/Group Roles"**
3. **Right-click "postgres"** → **Properties**
4. **Go to "Definition" tab**
5. **Set password:** `123456`
6. **Click Save**

