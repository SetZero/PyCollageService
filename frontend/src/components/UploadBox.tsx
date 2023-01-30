import * as React from 'react';
import Box from '@mui/material/Box';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import './style/UploadBox.css';
import { useRef, useState } from 'react';
import { CircularProgress, LinearProgress } from '@mui/material';

interface UploadBoxProps {
    onUpload: (file: FileList) => Promise<void>
}

// TODO: Move uploadFile and Gallery view to own Component / Utility class

function UploadBox(props: UploadBoxProps) {
    const acceptedFiles = ".zip";
    const uploadInputRef = useRef<HTMLInputElement>(null);
    const [uploadInProgress, setUploadInProgress] = useState(false);

    function handleUserUpload() {
        uploadInputRef.current?.click();
    }

    function uploadFile() {
        let file = uploadInputRef.current;
        if (file === null || file.files === null)
            return;

        setUploadInProgress(true);
        props
            .onUpload(file.files)
            .finally(() => {
                setUploadInProgress(false);
            });
    }

    function showProgress() {
        if (uploadInProgress) {
            return (<CircularProgress />);
        }
        return (<CloudUploadIcon />);
    }

    return (
        <Box className="wrapper">
            <form action="#" onClick={handleUserUpload}>
                <input className="file-input" type="file" name="file" hidden ref={uploadInputRef} accept={acceptedFiles} onChange={uploadFile} />
                {showProgress()}
                <p>Browse File to Upload</p>
            </form>
        </Box>
    )
}

export default UploadBox;