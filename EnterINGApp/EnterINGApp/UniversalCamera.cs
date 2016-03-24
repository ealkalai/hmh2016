using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.Media.Capture;
using Windows.Media.MediaProperties;
using Windows.UI.Xaml.Controls;

namespace EnterINGApp
{
    public class UniversalCamera

    {

        private static UniversalCamera _Default;

        public static UniversalCamera GetDefault()
        {
            if (_Default == null)
            {
                _Default = new UniversalCamera();
            }
            return _Default;
        }

        CaptureElement capturePreview;
        public MediaCapture captureMgr;
        ImageEncodingProperties imageProperties = ImageEncodingProperties.CreateJpeg();

        public async System.Threading.Tasks.Task InitPreview(CaptureElement capturePreview)
        {
            this.capturePreview = capturePreview;
            this.captureMgr = new MediaCapture();
            
            MediaCaptureInitializationSettings settings = new Windows.Media.Capture.MediaCaptureInitializationSettings();
            
            settings.StreamingCaptureMode = StreamingCaptureMode.Video;

            await this.captureMgr.InitializeAsync(settings);

            this.capturePreview.Source = captureMgr;
            this.captureMgr.SetPreviewRotation(VideoRotation.Clockwise90Degrees);
            
            await this.captureMgr.StartPreviewAsync();

        }

        public async System.Threading.Tasks.Task AutoFocus()
        {

            await this.captureMgr.VideoDeviceController.FocusControl.FocusAsync();
        }


       
    }
}
