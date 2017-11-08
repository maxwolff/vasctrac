// Load environment variables
require('dotenv').config({path: 'src/_env'});

const AWS_APP_ID = process.env.AWS_APP_ID;
const AWS_USER_ID = process.env.AWS_USER_ID;

module.exports = {
    AWS_APP_ID: AWS_APP_ID,
    AWS_USER_ID: AWS_USER_ID
}
