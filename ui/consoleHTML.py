content=r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    <meta charset="UTF-8">
    <title>Incognito BETA</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
        }

        body {
            display: block;
            background-color: #242424;
            color: #e2e2e2;
            font-family: "Inter", sans-serif;
            font-style: normal;
            font-weight: 300;
            overflow: hidden;
        }

        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
            margin-top: 4px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
            margin-top: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #303030;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #3b3b3b;
        }

        .top-bar {
            display: flex;
            align-items: center;
            padding: 7px;
            background-color: #282828;
            width: 100%;
        }

        .top-bar img {
            margin-right: 6px;
            height: 20px;
            width: 20px;
            cursor: pointer;
            display: flex;
            background-color: #303030;
            border-radius: 7px;
            padding: 9px;
            justify-content: space-between;
            box-shadow: inset 0 1px 2px 0 #ffffff14;
        }

        .search-container {
            display: flex;
            align-items: center;
            flex-grow: 1;
            position: relative;
        }

        .search-container input {
            width: 87%;
            background-color: #303030;
            padding: 13px 20px 10px 40px;
            border: none;
            box-shadow: inset 0 1px 2px 0 #ffffff14;
            border-radius: 4px;
            outline: none;
            color: white;
        } 

        .search-container .search-icon {
            position: absolute;
            left: 5px;
            pointer-events: none;
            box-shadow: none; 
            width: 16px;
            height: 16px;
        }

        .output {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 20px;
            width: 100%;
            height: 100%;
            font-size: 13px;
            font-weight: 500;
            overflow-y: scroll;
        }

        .message {
            color: white;
            z-index: 9999999;
        }

        .error {
            color: rgb(230, 61, 61);
        }

        .warning {
            color: #ffc251;
        }

    </style>
</head>
<body>
    <div class="top-bar">
        <img draggable="false" id="clear" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC4ElEQVR4nO2dS2sUQRRGC3WSOCv9Uy59gPj4JW4FF8atqPER8D8oTnTtVsHoRkTdGTdiVq6PXKyBYZzJdM+j6t5b90BgINXT1Ycv1elb1d0pBUEQBEEQBEsADIArwD7wAfgJHOXP+/l3g2W+O8gAN4FvLOYrcGO8XdAR4Axwn/48Bba67qdpgG1gxPIcADu1j0M1wBbwgtV5E7I3LzlkF5QcsgtKDtkFJYdsykluVzblJbcnm3qS25FNfcn+ZaNHsl/Z6JPsTzZ6JfuRzeoFolIcmK36oT/J0zxP1sBOkqexM3mAvSRP8t3EEILdJE9yKWkG20me5FnSCn4kC++TRvAlWThK2sCfZOFH0gQ+JQvvkhbwK1l4khT9C/cKv1ys7dh7koUv1dfxdUzyCLiDXa5ZSPLrcbkRuIU9HllJ8vbUdrexw6jqkNE3ydMYSfbc/puQbES2D8nKZfuSrFS2T8nKZPuWrER2G5Iry25LciXZbUouLLttyYVkh+QCsqtLHnSsXRTtJOutjfxXeykOsKc1Cawn2XWTnA/kuva7Tlkt2SqSLPdXf1adhNWSraP/stRJc5JXTHb9JI/Jd/7P4hAYJoXQbVpMj2RBljrN6ejlZHfB5EiVZEFW4Mzp7LmkDKxKXiD6fFIEliVbGTqAHdOSBVnqNKfjHzWcDPEgWZClTloPAC+SNV+woKSKWPoSvGhq8JRkrUUlPCZ5Rpm0aorwnGQtaeLfvl+6TbIG2bQmuYZsWpVcUjatSy4hm5C8edmE5M0nm5C8edmE5LXXhIczth3mOUjfFyOFZR9KPVtmafKPPG//U0jejOxSHAMPgLMLhr17+WULMqO0e9ITZfq2b0m28PiEvoqoaXbX1b412X+AUz3mRec+FqJv+yLkP7N5a0NK4lv0GOBqfu9JLfZ6DgV319W+OMBp4ALwEHgL/Cog+Hd+N8uik+FuTmrXk2Hn9kEQBEEQBEEQBMkCfwGKrZkBLi93JAAAAABJRU5ErkJggg==">
        <img draggable="false" id="copy" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACeElEQVR4nO3cP47TUBDHcQsQSwEcAKiRuMB2W9CsBOIadPwpOQiIi1Bwgl1EtcsZgIoKAYIUM1/kRKJKjBM/e8Z+v5/0ymycT+aNX0ZaN42iKIqiKMpiA9wAXmL2EbOfuDP6MlthdgYcNzUEuIfZp0lwt4P/Bk6bxVeyBSLXgk3bLqKRa8Cm7cnRwDVgY/YjCPRXVdhEVS6cdH7JZn+AJ81SQhD0+r1rwiYQuipsgqGrwSYBdBXYJIFePDaJoBeNTTLoxWKTEDo9dteoc27QbYCH6X5B/m/UOUfodNh9Rp1zhd4D+zjFqDMbNHCnMPZZEcyho86E0K/2/pxd2GarwZAlRp3poM1WLXbJyi6C2fnmPT7YkNcykyVoF3QTXYWqaI+HU+vweFT1aBe0Th1DM2RbkWDLq3V4PJ56tMfD9t21xaLW4YJGFb1J9HZX6/B4OPVoj0fVzdAFvTUkqERVtMfjqXV4vtWMnSEXQQIgQXs8nira42HVOlzQ6tFDopuh69SBevQm0Tcw3Qw9Hk6nDo9H1fHOBb01JKhEVbTH46l1eL7VjJ1eFwK3Uj0YxQsvs+9ZoO/P4lE/fjD0hyzQj7a+Fl6EI5VY8CwHtNmbHdBHmF3OvJovgOtZoD8D1zr+6/Zyxsh3R0fuDb3ZXk93/g04Ap63vS79DbK9PrPztl1MUsl7Q5t93XX6UHpkz2p4D1wV7AE5YOu9Bq4Ie2zoDfY74Lawx4b2Nfa39ZMRdpxGlFLQ/g/8C2ZvgcfAA+CmkEtWtOdbqb/gaBwEHQ/Hoio6+y85TzTqHBKNOieKRp0TRaPOCaNR54TRqFNRFEVRFEVRFKVZRv4CCvcHVDvEilYAAAAASUVORK5CYII=">
           
        <div class="search-container">
            <img class="search-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFKElEQVR4nO2cz29VRRTHjyYWgbKg/t4aowuJJoo/o5EFAUz8gf4dLbrTujLGRDdiC7o1Df4CEmJ0QYwhoERUWCu48QcEsRbbjQsF8n0fM/dd0LZ37nuvtG9m7ptPcjfty73nft95M2fOnDNmmUwmk8lkMplMJpNZDLAW2AqMI00hfYf0E9Ic0oXymiv/9m3xGfdZ2AKsqbhl5jLAzcCLSEcLIVstlnS1v4SjwAvunlceMOgAjyN9inRpyeL6Rb9Y3Bses0EFeALpq2UX1y/6l+5LtUEBuBVpD1KrbyLPF3w/cIs1GeD5YhILIXBrnthzwHZrGsAQ0mRPXiydQ/oQGCujiTuA9cB15bW+/Jv7347is9LvPdy/hfS2u5c1AWAY6YsuX34GaQK4/yqet7H8Us93+czPnY2WMsANSCe6eNnTwCiwehmfvbr4NUhnunj+cWerpYhbOCB900X4NbmSHlUILr2K9E8HW04k59nlmFw/XEg/AHf30aYNSCe7GEbSGbMLL61/oY9DLJVxS3sX3tXbttNSAHi6NrqQ3gGuDWjfNUhv1UYj8JwlsBjxx8nSLosEpN01ds5GnSdBer/DcBHMkxfibKkdRqQpizh3UT1kSN/HmL6kHeOfqhlC4ktGeRNELqzqY3TRK8A93rSsdNhiAnik5if4mkUO0hte+2Py6iLn61/xLdtqb4XDvrOed/jEotkZcSu8am8YtUTA7e74Vq9wU8wGzqTgzQtSBtWJKBiz0BT7c9VCT1hiIO3yvMuRGMa26hkb7rPEAB6oiZzC/TqLpHu1YecsQWgvz6c9jrM5pGGveIT+wBIFt4KtFvqlkEZNRTt5LJGiHqTaed6zUBRVQtVCb7FEAbZ5hD4WzijpF4/Qt1ui4DZ8q4X+OZxRLp1YLfSIpbzP2aoU+nw4o/yh3ZAlCm4bzhPihTOqmUKv8gh9IZxRzRw6bvQIPRvOqMGaDE/HGN5ttUQBnvQI/XWMC5Ydlij4s5F7Qho17jHqI0sUpL0e5xkPZ5TrM6kWetolaKxZSaVNoZPlvhBvoyUG8FDNLsvaWBP/k5YY+IpqpEMxZ7tmYqzl6PDr/DPavc8Om7NjDdmcvc0iLzc4k4JX096S+83zDvssFlyRSaWRbUNft8hBejOJAhpH0cfn39jcYJEC3FtTEhZ+EvR0wPqKHE8GD48qANYh/eix2bnzwxYjRaNmfSNlbGW7B5Ir23W4jtQOhei7LRKQ3q2x87xLl1rMAE81oLViu6VA0ZHqe5H/hpHhQGPygUY0CzmKFmLXSlb/QqdcEXifo4vqiW++XQfddpYltqQ91mVD57oVtqNzQ+fifsPrLbEW5eNdvNjZ8sSYNcsqcPtEm+oVXwM9e7jjMNL632zvSmfhwaXks4uJzqU6XRbOlyBquNhuzN7Z4zES02XLnPP0bcCd5dERQ+U1AtxV/s957l6kP3o8RsLZdLBRYjuAZ70lCq0+Xu04+ZnSplVNFXukPE9DgUTev7AnpTwk4LNGTZDzMn7S4T4KfKgud9FYz74M8KhrMfNuHlyduC583NdtqrPxYl8pxWqfGHOkp5h3sRCXSu8dXcrOyECIveCYns3Ay67SvjjJpn085mx5UuPF8sjMX10FUZE1bB+ZuWk50rEDJXZoGj1BxkYWu49ksftIFruPZLH7SBa7j+TQLz6xkzvdIU2xpb9SrBFPT2zp75jqWJordsgm/YaLPVEMF86TXX4mtZN7U6Lcs8zjciaTyWQymUwmYyvLv0pCOlhwmyxFAAAAAElFTkSuQmCC"> 
            <input type="text" placeholder="Search...">
        </div>
    </div>
    <div class="output">
    </div>
</body>
<script>
    const minimize = document.querySelector('#minimize')
    const closeButton = document.querySelector('#close');
    const clearButton = document.querySelector('#clear');
    const copyButton = document.querySelector('#copy');
    const outputContainer = document.querySelector('.output');
    const messageTypeMapping = {
        'Enum.MessageType.MessageOutput': 'message',
        'Enum.MessageType.MessageError': 'error',
        'Enum.MessageType.MessageWarning': 'warning'
    };

    function printMessage(message, type = 'Enum.MessageType.MessageOutput') {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        const timeString = `[${hours}:${minutes}:${seconds}]`;

        const escapeHtml = text => text.replace(/&/g, '&amp;')
                                    .replace(/</g, '&lt;')
                                    .replace(/>/g, '&gt;')
                                    .replace(/"/g, '&quot;')
                                    .replace(/'/g, '&#039;')
                                    .replace(/\n/g, '<br>'); 
                                    
        const formattedMessage = escapeHtml(message);

        const fullMessage = `${timeString} ${formattedMessage}`;
        const messageDiv = document.createElement('div');

        const className = messageTypeMapping[type] || 'message';
        messageDiv.className = className;
        messageDiv.innerHTML = fullMessage; 
        messageDiv.style.whiteSpace = 'pre-wrap';

        outputContainer.appendChild(messageDiv);
    }

    if (clearButton && copyButton) {
        clearButton.addEventListener('click', () => {
            outputContainer.innerHTML = '';
        });

        copyButton.addEventListener('click', () => {
            const textToCopy = Array.from(outputContainer.children)
                                    .map(elem => elem.textContent
                                    .replace(/^\[\d{2}:\d{2}:\d{2}\]\s*/, ''))
                                    .join('\n');

            const textarea = document.createElement('textarea');
            
            textarea.value = textToCopy;
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                console.log('Content copied');
            } catch (err) {
                console.log('Failed to copy: ' + err, 'error');
            }
            document.body.removeChild(textarea);
        });
    }

</script>
</html>

"""
