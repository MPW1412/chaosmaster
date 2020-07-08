import axios from './index';

export default{
    getStoreObjectImages(uuid) {
        return axios.get(`images/${uuid}/`)
            .then(response => {
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    addImageToStoreObject(uuid, param){
        return axios.post(`images/${uuid}/`, param)
            .then(response => {
                console.log(response.data)
                // JSON responses are automatically parsed.
                return response.data;
            })
            .catch((e) => {
                console.log(e)
                return e;
            });
    },

    deleteImageById(id){
        return axios.delete(`images/change/${id}/`)
        .then(response => {
            console.log(response.data)
            // JSON responses are automatically parsed.
            return response.data;
        })
        .catch((e) => {
            console.log(e)
            return e;
        });

    }
}