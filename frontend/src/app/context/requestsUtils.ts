import axiosInstance from "./axiosInstance";


/**
 * Processes text input for general pathfinding.
 * @param {string} text - Text to process.
 * @returns {object} - Response data.
 */
export const processPathfinding = async (text:string) => {
    try {
        const data = { text };
        const response = await axiosInstance.post("/general/process", data);
        return response.data;
    } catch (err:any) {
        console.error("Error in processPathfinding:", err.response?.data || err.message);
        throw err;
    }
};


/**
 * Processes an audio file and returns its transcript.
 * @param {File} audioFile - Audio file to process.
 * @returns {object} - Response data with transcript.
 */
export const processAudio = async (audioFile:File) => {
    try {
        const formData = new FormData();
        formData.append("file", audioFile);

        const response = await axiosInstance.post("/stt/", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return response.data;
    } catch (err:any) {
        console.error("Error in processAudio:", err.response?.data || err.message);
        throw err;
    }
};
