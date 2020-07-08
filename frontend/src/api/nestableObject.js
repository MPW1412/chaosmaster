import axios from './index';

export default{
    getNestableObject() {
        return axios.get(`nestable-objects/`)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    createNestableObject(param) {
        return axios.post(`nestable-objects/`, param)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    getNestableObjectByUUID(uuid){
        return axios.get(`nestable-objects/${uuid}` )
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    }
}    