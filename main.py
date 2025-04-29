<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MR DEVIL GROUP UID FINDER</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #00ff00;
        }

        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            background-color: #111;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-size: 16px;
            border-radius: 5px;
        }

        button:hover {
            background-color: #0f0;
            color: #000;
        }

        #result {
            margin-top: 20px;
            white-space: pre-wrap;
            background: #111;
            padding: 10px;
            border: 1px solid #0f0;
            border-radius: 5px;
        }
    </style>
</head>
<body>

<h1>MR DEVIL GROUP UID FINDER</h1>

<input type="text" id="token" placeholder="Enter your Facebook Access Token">
<button onclick="getGroups()">Get Group UIDs</button>

<div id="result">Group UIDs will appear here...</div>

<script>
    async function getGroups() {
        const token = document.getElementById("token").value;
        const resultDiv = document.getElementById("result");
        resultDiv.innerText = "Fetching groups, please wait...";

        try {
            const res = await fetch(`https://graph.facebook.com/me/groups?access_token=${token}`);
            const data = await res.json();

            if (data.error) {
                resultDiv.innerText = "Error: " + data.error.message;
                return;
            }

            if (!data.data || data.data.length === 0) {
                resultDiv.innerText = "No groups found or token doesn't have permission.";
                return;
            }

            let output = "Your Groups:\n\n";
            data.data.forEach(group => {
                output += `Name: ${group.name}\nUID: ${group.id}\n\n`;
            });

            resultDiv.innerText = output;
        } catch (e) {
            resultDiv.innerText = "Failed to fetch groups. Make sure token is correct.";
        }
    }
</script>

</body>
</html>
