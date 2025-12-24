"use client";
import { createContext, useContext, useState, useEffect } from 'react';
import { ethers } from 'ethers';

const Web3Context = createContext();

export function Web3Provider({ children }) {
  const [account, setAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [chainId, setChainId] = useState(null);

  useEffect(() => {
    const init = async () => {
      if (window.ethereum) {
        console.log("Initializing Web3 Provider...");
        const provider = new ethers.BrowserProvider(window.ethereum);
        setProvider(provider);
        console.log("Provider set.");

        try {
          const accounts = await provider.listAccounts();
          if (accounts.length > 0) {
            setAccount(accounts[0].address);
          }
          const network = await provider.getNetwork();
          setChainId(network.chainId);
          console.log("Network detected:", network.chainId);
        } catch (e) {
          console.error("Error auto-connecting:", e);
        }
        
        window.ethereum.on('accountsChanged', (accounts) => {
          console.log("Accounts changed:", accounts);
          setAccount(accounts[0] || null);
        });
        
        window.ethereum.on('chainChanged', (id) => {
          console.log("Chain changed:", id);
          setChainId(id);
          window.location.reload();
        });
      } else {
        console.error("Window.ethereum not found. Install MetaMask.");
      }
    };
    init();
  }, []);

  const connectWallet = async () => {
    let currentProvider = provider;
    
    // Lazy check: If provider wasn't found on mount, try to find it now
    if (!currentProvider && window.ethereum) {
      console.log("Lazy initializing provider...");
      currentProvider = new ethers.BrowserProvider(window.ethereum);
      setProvider(currentProvider);
    }

    if (!currentProvider && !window.ethereum) {
      alert("MetaMask not found! Please install the MetaMask extension for your browser.");
      window.open("https://metamask.io/download/", "_blank");
      return;
    }

    try {
      // Use currentProvider (local var) or provider (state)
      const prov = currentProvider || new ethers.BrowserProvider(window.ethereum); 
      
      console.log("Requesting accounts...");
      const accounts = await prov.send("eth_requestAccounts", []);
      setAccount(accounts[0]);
      
      const signer = await prov.getSigner();
      setSigner(signer);
      
      const network = await prov.getNetwork();
      setChainId(network.chainId);
      console.log("Connected:", accounts[0], "Chain:", network.chainId);
    } catch (err) {
      console.error("Wallet connection failed:", err);
      alert("Connection failed: " + err.message);
    }
  };

  return (
    <Web3Context.Provider value={{ account, provider, signer, chainId, connectWallet }}>
      {children}
    </Web3Context.Provider>
  );
}

export const useWeb3 = () => useContext(Web3Context);
