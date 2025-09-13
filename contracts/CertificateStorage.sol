// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateStorage {
    // Mapping to store certificate hashes (CertID => Hash)
    mapping(string => bytes32) private certificateHashes;
    // Mapping to store certificate metadata
    mapping(string => Certificate) private certificateDetails;

    // Struct for certificate metadata
    struct Certificate {
        string name;
        string eventName; // Changed from 'event' to 'eventName'
        string date;
        bytes32 hash;
    }

    // Event for logging certificate storage
    event CertificateStored(string certID, bytes32 hash, string name, string eventName, string date);

    // Store a certificate hash
    function storeCertificate(
        string memory certID,
        bytes32 certHash,
        string memory name,
        string memory eventName, // Updated
        string memory date
    ) public {
        require(certificateHashes[certID] == bytes32(0), "Certificate ID already exists");
        certificateHashes[certID] = certHash;
        certificateDetails[certID] = Certificate(name, eventName, date, certHash);
        emit CertificateStored(certID, certHash, name, eventName, date);
    }

    // Verify a certificate hash
    function verifyCertificate(string memory certID, bytes32 certHash) public view returns (bool) {
        return certificateHashes[certID] == certHash;
    }

    // Get certificate details for validation portal
    function getCertificateDetails(string memory certID) public view returns (string memory, string memory, string memory, bytes32) {
        Certificate memory cert = certificateDetails[certID];
        return (cert.name, cert.eventName, cert.date, cert.hash); // Updated
    }
}