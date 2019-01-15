var jwt = require('jwt-simple');  
var moment = require('moment');  
var config = require('../configs/config');

exports.ensureAuthenticated = function(req, res, next) {  
  if(!req.headers.authorization) {
    return res.status(403).send({message: "Authorization error"});
  }
  
  var token = req.headers.authorization;
  
  try{
    var payload = jwt.decode(token, config.TOKEN_SECRET);
  }
  catch(err){
    return res.status(401).send({ message: "Authorization error", error: err.message });
  }

  if(payload.exp <= moment().unix()) {
     return res.status(401).send({message: "The token expires"});
  }

  req.user = payload.sub;
  next();
}
//https://github.com/sahat/satellizer/blob/master/examples/server/node/server.js