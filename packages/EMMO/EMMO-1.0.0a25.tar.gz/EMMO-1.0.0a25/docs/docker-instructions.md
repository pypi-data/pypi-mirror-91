# EMMO-python Docker

### Clone project

```bash
git clone git@github.com:emmo-repo/EMMO-python.git
```

### Build Docker image

```bash
cd EMMO-python
docker build -t emmo .
```

### Run Docker container

```bash
docker run -it emmo
```

### Notes

* Your Docker container may run out of memory while executing HermiT
  (``sync_reasoner``). Append ``--memory=2GB`` to ``docker run`` in
  order to align the memory limit with the Java runtime environment.

* Uncomment the last line in Dockerfile if you wish to start directly
  in python. 


### Dockerfile for mounting EMMO-python as volume (mount.Dockerfile)

### Build docker image

```bash
docker build -t emmomount -f mount.Dockerfile .
```

### Run Docker container
```bash
docker run --rm -it -v $(pwd):/home/user/EMMO-python emmomount (linux)
```

```PowerShell
docker run --rm -it -v ${PWD}:/home/user/EMMO-python emmomount (windows10, Powershell)
```

To install EMMO-python package inside container:
```bash
cd EMMO-python
pip install .
```

### Notes on mounting on windows

* Allow for mounting of C: in Docker (as administrator)
  Docker (rightclick in system tray)->Settings->Shared Drives->tick of C->Apply

* Run the following command in Powershell: 
```Powershell
Set-NetConnectionProfile -interfacealias "vEthernet (DockerNAT)" -NetworkCategory Private
```
* If mounting does not succeed Reset Credentials (Docker -> Settings -> Shared Drives)  and repeat the steps above.

