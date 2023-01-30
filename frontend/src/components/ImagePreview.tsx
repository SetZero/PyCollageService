import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';
import { useState } from 'react';
import './style/ImagePreview.css';

export interface ImageInfo {
    img: string,
    title: string,
    author: string
}

interface ImagePreviewProps {
    imageList: ImageInfo[]
}

function ImagePreview(props: ImagePreviewProps) {

    return (
        <ImageList cols={1} className="image-preview">
                <ImageListItem key="Subheader" cols={3}>
                    <ListSubheader component="div">Your Images</ListSubheader>
                </ImageListItem>
                {props.imageList.map((item) => (
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
    )
}

export default ImagePreview;