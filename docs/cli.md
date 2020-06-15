# `lootmarshal`

**Usage**:

```console
$ lootmarshal [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `connect`: Connects to a specified handler
* `creds`: Interact with creds
* `secret`: Interact with secrets
* `server`: Starts the LootMarshal server

## `lootmarshal connect`

Connects to a specified handler

**Usage**:

```console
$ lootmarshal connect [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `azure`: Connects to Azure.

### `lootmarshal connect azure`

Connects to Azure.

**Usage**:

```console
$ lootmarshal connect azure [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `lootmarshal creds`

Interact with creds

**Usage**:

```console
$ lootmarshal creds [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `lsass`: Parses lsass dump for creds.

### `lootmarshal creds lsass`

Parses lsass dump for creds. 

**Usage**:

```console
$ lootmarshal creds lsass [OPTIONS]
```

**Options**:

* `-f `: Path to LSASS dump  [required]
* `-s`: Save creds to secretclient
* `--help`: Show this message and exit.

## `lootmarshal secret`

Interact with secrets

**Usage**:

```console
$ lootmarshal secret [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Gets a secret.
* `list`: Lists all secret.
* `set`: Sets a secret.

### `lootmarshal secret get`

Gets a secret.

**Usage**:

```console
$ lootmarshal secret get [OPTIONS] NAME
```

**Options**:

* `--help`: Show this message and exit.

### `lootmarshal secret list`

Lists all secret.

**Usage**:

```console
$ lootmarshal secret list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `lootmarshal secret set`

Sets a secret.

**Usage**:

```console
$ lootmarshal secret set [OPTIONS]
```

**Options**:

* `-n `: Name of the secret  [required]
* `-v `: Value of the secret  [required]
* `-c `: Content type of the secret  [required]
* `--help`: Show this message and exit.

## `lootmarshal server`

Starts the LootMarshal server

**Usage**:

```console
$ lootmarshal server [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
