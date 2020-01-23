# Go-Back-N and Selective Repeat ARQs 

GBN and SR ARQ point to point protocols implementation

## Description
This program imitates transmission between receiver and transmitter (p2p) by GBN or SR protocols.
For receiver and transmitter creates processes (by multiprocessing python library).

Program includes:
	- GBN and SR ARQ protocols (api) class -- ***PointToPoint***
	- Test shell file with some tests

The main class ***PointToPoint*** is in [connections.py](https://github.com/LesikDee/Computer_Network/blob/master/P2P_GBN_SR/src/connections.py) file.
***PointToPoint*** contains such constructor, that defines character of transmission:
	- `protocol_type: str` 'gbn' or 'sr'
	- `window_size: int` 
	- `lose_prob: float` probability of lose the packet (as for receiver as for transmitter)
	- `transfer_number=-1`
	- `seconds=-1`

**Note**: ***one and only one*** of the parameters `transfer_number` and `seconds` must be in the constructor. Presence one of these parameters define the transmission *mode*:
	-`transfer_number` means that transmission will be until *transfer_number* packets are transmitted
	-`seconds` means that transmission will be performed for *seconds* seconds

## Usage 

To start the transmission one needs to create an instance of ***PointToPoint*** class and call `start_transmission()` method of this class;
#####Example:
```python
if __name__ == '__main__':
    window_size = 4
    lose_prob = 0.5
    conn = PointToPoint('gbn', window_size, lose_prob, seconds=20)
    conn.start_transmission()
```

To see transmission dialog in the console it is necessary to define field `_debug` into `True` state
## Tests 

The test shell includes two methods (`arq_test_shell` and  `stat_plot`) and allows us to know the time of transmission in seconds or number of the transmitted packets.
Using this method it is easy to create your own tests, for ***example***: 
```python
def test_pack_lose():
    lose_pr = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # lose probability list
    sr_pack = arq_test_shell(lose_pr, 4, 'sr', test_mode='number', window_size=4, session_seconds=20)
    gbn_pack = arq_test_shell(lose_pr, 4, 'gbn', test_mode='number', window_size=4, session_seconds=20)

    stat_plot(lose_pr, gbn_pack, sr_pack,
              'Package lose probability', 'Packages transferred', '../results/pack_lose.png')
```