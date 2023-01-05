import React from "react";
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';


const Toast = ({message, status}) => {
    return (
        <Snackbar open={true} autoHideDuration={6000}>
            <Alert severity={status} sx={{ width: '100%' }}>
                {message}
            </Alert>
        </Snackbar>
    )
}

export default Toast;