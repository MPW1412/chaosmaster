import axios from './index';

export default{
    myData() {
        return axios.get(`bpi/currentprice.json`)
            .then(response => {
                // JSON responses are automatically parsed.
                return response;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    }
}