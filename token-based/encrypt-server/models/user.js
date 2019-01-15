var mongoose = require('mongoose');
var bcrypt = require('bcryptjs');

var Schema = new mongoose.Schema({
	name: { 
    type: String, 
    unique: true,
    required: true
  }, 
  email: { 
    type: String, 
    unique: true, 
    lowercase: true,
    required: true
  },
  /*password: { 
    type: String, 
    select: false 
  }*/
})

/*Schema.pre('save', function(next) {
  var user = this;
  if (!user.isModified('password')) {
    return next();
  }
  bcrypt.genSalt(10, function(err, salt) {
    bcrypt.hash(user.password, salt, function(err, hash) {
      user.password = hash;
      next();
    });
  });
});*/

Schema.methods.comparePassword = function(password, done) {
  bcrypt.compare(password, this.password, function(err, isMatch) {
    done(err, isMatch);
  });
};

var User = mongoose.model('User', Schema);
module.exports = User;

/*
module.exports = mongoose.model('User', new Schema({ 
    username: { type: String, unique: true }, 
    email: { type: String, unique: true, lowercase: true },
    password: { type: String, select: false }
}));
*/