var mongoose = require('mongoose');

var Schema = new mongoose.Schema({
  name: {
    type: String,
  },
  urlFrom: {
    type: String
  },
  urlTo: {
    type: String
  },
  service: {
    type: String
  },
  used: {
  	type: Date,
  	default: Date.now
  }
})

var encryp = mongoose.model('encryp', Schema);
module.exports = encryp;

/*
module.exports = mongoose.model('User', new Schema({ 
    username: { type: String, unique: true }, 
    email: { type: String, unique: true, lowercase: true },
    password: { type: String, select: false }
}));
*/