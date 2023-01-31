import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import UploadBox from './UploadBox';
import './style/MainCenterBox.css'
import ImagePreview, { ImageInfo } from './ImagePreview';
import { useState } from 'react';
import { Alert, Container } from '@mui/material';
import UploadStepper from './UploadStepper';

function MainCenterBox() {
  let imageList: ImageInfo[] = [];
  const [images, setImages] = useState(imageList);
  const [errors, setErrors] = useState({ show: false, error: "" });

  function uploadHandler(files: FileList): Promise<void> {
    setErrors({ show: false, error: "" });

    let data = new FormData();
    data.append('file', files[0]);
    data.append('collage_image', '1b66debf1c09244aeb8dc503d676a953e091c5a8.jpg');
    return new Promise((resolve, reject) => {

      fetch('http://127.0.0.1:8085/api/v1/collage', {
        method: 'POST',
        body: data
      })
        .then(response => {
          if (!response.ok) {
            throw response.json()
          }
          return response.blob();
        })
        .then(imageBlob => {
          const imageObjectURL = URL.createObjectURL(imageBlob);
          console.log(imageObjectURL);
          setImages(images => [...images, { img: imageObjectURL, author: '', title: 'Your Image' }]);
          resolve();
        })
        .catch((e) => {
          e.then((err: any) => {
            setErrors({ show: true, error: err.status });
          })
          reject();
        })
    });
  }

  function showError() {
    if (errors.show)
      return (<Alert severity="error">{errors.error}</Alert>);
    return (<span />);
  }

  return (
    <Card sx={{ minWidth: 275 }} className="main-center-box">
      {showError()}
      <CardContent>
        <Typography variant="h4" component="div" className='header'>
          Image to Collage
        </Typography>
        <Container maxWidth="sm">
          <UploadBox onUpload={uploadHandler} />
          <ImagePreview imageList={images} />
        </Container>
        <Container>
          <UploadStepper />
        </Container>
      </CardContent>
      <CardActions>
        <Button size="small">About</Button>
        <Button size="small">Contact</Button>
      </CardActions>
    </Card>
  );
}

export default MainCenterBox;