import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import UploadBox from './UploadBox';
import './style/MainCenterBox.css'

function MainCenterBox() {
    return (
        <Card sx={{ minWidth: 275 }} className="main-center-box">
          <CardContent>
            <Typography variant="h4" component="div" className='header'>
              Image to Collage
            </Typography>
            <UploadBox />
          </CardContent>
          <CardActions>
            <Button size="small">About</Button>
            <Button size="small">Contact</Button>
          </CardActions>
        </Card>
    );
}

export default MainCenterBox;