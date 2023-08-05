# PyGeth

PyGeth is a Python library for a quick setup of an Ethereum blockchain using Geth and for fast prototyping of contracts with truffle.

## Installation

### Prerequisites

To be able to run this package, please install [Geth](https://geth.ethereum.org/downloads/) and [Npm (5.2.0 or higher)](https://www.npmjs.com/) 
and add them to your Path. 
**Note:** This has solely been tested on Windows.


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install *python-geth*.
<br>

```bash
pip install python-geth
```

## Usage

### Node

```python
from python_geth.node import Node

node1 = Node(datadir="C:\\Users\\macutko\\Desktop\\node01")
node1.start_node()

```
This creates a geth node that allows interaction with it via the web3 library.

```python
node1.w3.geth.miner.start(1)
``` 

To add a node on the chain do as follows. It requires the same genesis file.

```python
node2 = Node(datadir="C:\\Users\\macutko\\Desktop\\node02", genesis_file="C:\\Users\\macutko\\Desktop\\node01\\config\\genesisjson")
node2.start_node()
node1.add_node(node2.w3.geth.admin.node_info()['enode'])
```

### Contracts

To be able to quickly deploy contracts and interact with them first configure truffle.

```python
node1.configure_truffle()
```

To deploy a contract unlock an account, create a Contract Interface instance and deploy a contract.
```python
account, password = node1.get_first_account()
node1.w3.geth.personal.unlock_account(account, password)

CI = ContractInterface(w3=node1.w3, datadir="C:\\Users\\macutko\\Desktop\\node01")
m_con = CI.deploy_contract(contract_file="C:\\Users\\macutko\\Desktop\\GUID.sol",constructor_params=['2265072m'])[0]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)