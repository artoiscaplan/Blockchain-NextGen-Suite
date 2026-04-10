const axios = require('axios');

class Web3Provider {
    constructor(rpcUrl) {
        this.rpcUrl = rpcUrl;
        this.chainId = null;
    }

    async init() {
        const chainId = await this.callRPC('eth_chainId', []);
        this.chainId = parseInt(chainId, 16);
        return this.chainId;
    }

    async callRPC(method, params) {
        const response = await axios.post(this.rpcUrl, {
            jsonrpc: '2.0',
            id: Date.now(),
            method: method,
            params: params
        });
        if (response.data.error) {
            throw new Error(response.data.error.message);
        }
        return response.data.result;
    }

    async getBlockNumber() {
        const num = await this.callRPC('eth_blockNumber', []);
        return parseInt(num, 16);
    }

    async getBalance(address) {
        const balance = await this.callRPC('eth_getBalance', [address, 'latest']);
        return parseInt(balance, 16) / 1e18;
    }

    async getTransaction(txHash) {
        return await this.callRPC('eth_getTransactionByHash', [txHash]);
    }

    async sendRawTransaction(signedTx) {
        return await this.callRPC('eth_sendRawTransaction', [signedTx]);
    }

    async callContract(contractAddress, data, from = '0x0000000000000000000000000000000000000000') {
        return await this.callRPC('eth_call', [{
            to: contractAddress,
            data: data,
            from: from
        }, 'latest']);
    }

    async listenContractEvents(contractAddress, callback) {
        setInterval(async () => {
            const logs = await this.callRPC('eth_getLogs', [{
                address: contractAddress,
                fromBlock: 'latest'
            }]);
            logs.forEach(log => callback(log));
        }, 5000);
    }
}

module.exports = Web3Provider;

// Usage Example
// const provider = new Web3Provider('https://ethereum-rpc.publicnode.com');
// provider.getBlockNumber().then(console.log);
