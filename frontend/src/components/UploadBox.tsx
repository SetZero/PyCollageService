import * as React from 'react';
import Box from '@mui/material/Box';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import './style/UploadBox.css';
import { useRef, useState } from 'react';

import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';

interface ImageInfo {
    img: string,
    title: string,
    author: string
}

// TODO: Move uploadFile and Gallery view to own Component / Utility class

function UploadBox() {
    const acceptedFiles = ".zip";
    const uploadInputRef = useRef<HTMLInputElement>(null);
    let imageList: ImageInfo[] = [];
    const [images, setImages] = useState(imageList);

    function handleUserUpload() {
        uploadInputRef.current?.click();
    }

    function uploadFile() {
        let file = uploadInputRef.current;
        if (file === null || file.files === null)
            return;

        let data = new FormData();
        data.append('file', file.files[0]);
        data.append('collage_image', '1b66debf1c09244aeb8dc503d676a953e091c5a8.jpg');

        fetch('http://127.0.0.1:8085/api/v1/collage', {
            method: 'POST',
            body: data
        })
            .then(response => response.blob())
            .then(imageBlob => {
                const imageObjectURL = URL.createObjectURL(imageBlob);
                console.log(imageObjectURL);
                setImages(images => [...images, {img: imageObjectURL, author: '', title: 'Your Image'}]);
            });
    }

    return (
        <Box className="wrapper">
            <form action="#" onClick={handleUserUpload}>
                <input className="file-input" type="file" name="file" hidden ref={uploadInputRef} accept={acceptedFiles} onChange={uploadFile} />
                <CloudUploadIcon />
                <p>Browse File to Upload</p>
            </form>

            <ImageList cols={1}>
                <ImageListItem key="Subheader" cols={3}>
                    <ListSubheader component="div">Your Images</ListSubheader>
                </ImageListItem>
                {images.map((item) => (
                    <ImageListItem key={item.img}>
                        <img
                            src={`${item.img}`}
                            srcSet={`${item.img}`}
                            alt={item.title}
                            loading="lazy"
                        />
                        <ImageListItemBar
                            title={item.title}
                            subtitle={item.author}
                            actionIcon={
                                <IconButton
                                    sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                                    aria-label={`info about ${item.title}`}
                                >
                                    <InfoIcon />
                                </IconButton>
                            }
                        />
                    </ImageListItem>
                ))}
            </ImageList>
        </Box>
    )
}

export default UploadBox;