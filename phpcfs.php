<?php
function EncryptDetails($value, $type){  
   $ciphering = "AES-128-CTR";   
   $options = 0;  
   $encryption_iv = '1234567891011121';  
   $encryption_key = $type;  
   return openssl_encrypt($value, $ciphering, $encryption_key, $options, $encryption_iv);
}

function DecryptDetails($value, $type){  
   $ciphering = "AES-128-CTR";  
   $options = 0;  
   $decryption_iv = '1234567891011121';  
   $decryption_key = $type;  
   return openssl_decrypt($value, $ciphering, $decryption_key, $options, $decryption_iv);
}

if ($argc > 2) {
    if ($argv[1] === 'encrypt') {
        echo EncryptDetails($argv[2], $argv[3]);
    } elseif ($argv[1] === 'decrypt') {
        echo DecryptDetails($argv[2], $argv[3]);
    }
}
?>