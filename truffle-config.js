const HDWalletProvider = require("@truffle/hdwallet-provider");
require("dotenv").config();

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545, // Use 8545 for Ganache CLI, 7545 for GUI
      network_id: "*",
    },
    mumbai: {
      provider: () => new HDWalletProvider(process.env.MNEMONIC, "https://rpc-mumbai.maticvigil.com"),
      network_id: 80001,
      gas: 5500000,
      gasPrice: 10000000000, // 10 Gwei
    },
  },
  compilers: {
    solc: {
      version: "0.8.0", // Matches your compilation
    },
  },
};