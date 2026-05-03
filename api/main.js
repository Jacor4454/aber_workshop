const express = require('express');
const path = require('path');
const app = express();

// Middleware for parsing JSON
app.use(express.json());

let users = [
  { username: "Jacor4454", name: 'Jacob Moore', title: "wizzard", img: './img1.png', met: []},
  { username: "OtherUser", name: 'John Doe', title: "deceased", img: './img2.png', met: [] },
];

app.get('/name', (req, res) => {

    if(req.headers.username == null){
        console.log("no user provided")
        return res.status(404).json({ message: 'User not provided' });
    }
    
    const user = users.find(u => u.username === req.headers.username)
    if (!user){
        console.log("no user found")
        return res.status(404).json({ message: 'User not found' });
    }
    
    return res.send(user["name"]);
});

app.get('/title', (req, res) => {

    if(req.headers.username == null){
        console.log("no user provided")
        return res.status(404).json({ message: 'User not provided' });
    }
    
    const user = users.find(u => u.username === req.headers.username)
    if (!user){
        console.log("no user found")
        return res.status(404).json({ message: 'User not found' });
    }
    return res.send(user["title"]);
});

app.get('/img', (req, res) => {
    const options = {
        root: path.join(__dirname)
    };

    if(req.headers.username == null){
        console.log("no user provided")
        return res.status(404).json({ message: 'User not provided' });
    }
    
    const fname = users.find(u => u.username === req.headers.username)

    if (!fname){
        console.log("no img found")
        return res.status(404).json({ message: 'User img found' });
    }

    return res.sendFile(fname.img, options);
});

// POST - Create a new user
app.get('/met', (req, res) => {

    if(req.headers.username == null){
        console.log("no user provided")
        return res.status(404).json({ message: 'User not provided' });
    }

    const user = users.find(u => u.username === req.headers.username)
    user['met'] = user['met'] + ":" + req.headers.other

    console.log(req.headers.username, "met", req.headers.other)

    return res.status(201).send("added " + req.headers.other);
});

// // PUT - Update a user completely
// app.put('/api/users/:id', (req, res) => {
//   const user = users.find(u => u.id === parseInt(req.params.id));
//   if (!user) return res.status(404).json({ message: 'User not found' });

//   user.name = req.body.name;
//   user.email = req.body.email;

//   res.json(user);
// });

// // DELETE - Remove a user
// app.delete('/api/users/:id', (req, res) => {
//   const userIndex = users.findIndex(u => u.id === parseInt(req.params.id));
//   if (userIndex === -1) return res.status(404).json({ message: 'User not found' });

//   const deletedUser = users.splice(userIndex, 1);
//   res.json(deletedUser[0]);
// });

app.listen(4041, () => {
  console.log('REST API server running on port 4041');
});
