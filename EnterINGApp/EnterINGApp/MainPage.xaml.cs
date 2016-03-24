using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading.Tasks;
using Windows.Devices.Enumeration;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.Media.Capture;
using Windows.Media.MediaProperties;
using Windows.Storage.Streams;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Media.Imaging;
using Windows.UI.Xaml.Navigation;
using ZXing;
using Windows.Security.Cryptography;
using Windows.Security.Cryptography.Core;
using System.Net.Http.Headers;
using System.Net.Http;
using Windows.UI.Popups;
using Windows.Storage;
using System.Threading;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace EnterINGApp
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        DeviceData data;
        DeviceData data2;
        string robin = "http://172.16.33.166:5000/response";
        string jens = "http://172.16.33.183:5000/response";
        string server;
        UniversalCamera camera;
        DispatcherTimer timer;
        QRCodeData qrdata;



        public MainPage()
        {
            this.InitializeComponent();

            server = robin;
            var device = "123456";
            var user = "Erikos A.";
            var pin = "123";
            var hashedPin = GetHashString(pin);

            data = new DeviceData(device, user, hashedPin);



            var device2 = "123456";
            var user2 = "Robin R.";
            var pin2 = "321";
            var hashedPin2 = GetHashString(pin2);

            data2 = new DeviceData(device2, user2, hashedPin2);
        }

        private async void Page_Loaded(object sender, RoutedEventArgs e)
        {
            camera = UniversalCamera.GetDefault();
            await camera.InitPreview(capturePreview);

            timer = new DispatcherTimer();
            timer.Interval = new TimeSpan(0, 0, 1);
            timer.Tick += Timer_Tick;
            await camera.AutoFocus();
            timer.Start();

        }

        //scann the picture every x seconds
        private async void Timer_Tick(object sender, object e)
        {
            timer.Stop();
            textBlockSessionInfo.Text = "point @ QR code";

            ImageEncodingProperties imgFormat = ImageEncodingProperties.CreateJpeg();
            // create storage file in local app storage 
            StorageFile file = await ApplicationData.Current.LocalFolder.CreateFileAsync(
            "temp.jpg",
            CreationCollisionOption.GenerateUniqueName);

            //await camera.AutoFocus();

            // take photo 
            await camera.captureMgr.CapturePhotoToStorageFileAsync(imgFormat, file);
            // Get photo as a BitmapImage 
            BitmapImage bmpImage = new BitmapImage(new Uri(file.Path));
            bmpImage.CreateOptions = BitmapCreateOptions.IgnoreImageCache;

            WriteableBitmap wrb;
            ZXing.BarcodeReader br;
            Result res;
            using (IRandomAccessStream fileStream = await file.OpenAsync(FileAccessMode.Read))
            {
                wrb = await Windows.UI.Xaml.Media.Imaging.BitmapFactory.New(1, 1).FromStream(fileStream);
            }

            br = new BarcodeReader { PossibleFormats = new BarcodeFormat[] { BarcodeFormat.QR_CODE } };
            br.AutoRotate = true;
            br.Options.TryHarder = true;

            
            res = br.Decode(wrb.ToByteArray(), wrb.PixelWidth, wrb.PixelWidth, RGBLuminanceSource.BitmapFormat.RGBA32);

            if (res != null)
            {
                try
                {
                    qrdata = Newtonsoft.Json.JsonConvert.DeserializeObject<QRCodeData>(res.Text);
                    textBoxSessionId.Text = qrdata.uuid;

                    textBlockSessionInfo.Text = qrdata.text;
                    textBlockSessionInfoExtra.Text = res.Text;

                    await camera.captureMgr.StopPreviewAsync();
                    capturePreview.Visibility = Visibility.Collapsed;
                }
                catch (Exception jsonEx)
                {
                    textBoxSessionId.Text = "error " + jsonEx.Message;
                    timer.Start();
                }

            }
            else
                timer.Start();

        }



        //hashing algorithm
        public static string GetHashString(string inputString)
        {
            var bufferString = CryptographicBuffer.ConvertStringToBinary(inputString, BinaryStringEncoding.Utf8);
            var hashAlgorithmProvider = HashAlgorithmProvider.OpenAlgorithm(HashAlgorithmNames.Md5);

            var bufferHash = hashAlgorithmProvider.HashData(bufferString);

            return CryptographicBuffer.EncodeToHexString(bufferHash);
        }


        //Get pin, verify, and submit
        private async void buttonSubmit_Click(object sender, RoutedEventArgs e)
        {
            DeviceData dataInput = data;
            var pin = textBoxPin.Password;
            var pinHashed = GetHashString(pin);
            var validate = dataInput.ValidatePin(pinHashed);
            if (!validate)
                dataInput = data2;
            validate = dataInput.ValidatePin(pinHashed);
            var uuid = textBoxSessionId.Text;
            if (!validate)
                textBlockSessionInfo.Text = "Wrong PIN\n";
            else
            {
                textBlockSessionInfo.Text = "Pin accepted by " + dataInput.UserId + "\n";

                var httpClient = new System.Net.Http.HttpClient();
                try
                {
                    this.buttonSubmit.IsEnabled = false;



                    string resourceAddress = server;
                    ResponseData responseData = new ResponseData();
                    responseData.device = dataInput.DeviceId;
                    responseData.user = dataInput.UserId;
                    responseData.uuid = qrdata.uuid;
                    responseData.service_id = qrdata.service_id;
                    responseData.something_generic = qrdata.something_generic;

                    string postBody = Newtonsoft.Json.JsonConvert.SerializeObject(responseData);
                    httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                    HttpResponseMessage wcfResponse = await httpClient.PostAsync(resourceAddress, new StringContent(postBody, Encoding.UTF8, "application/json"));

                    textBoxPin.Password = "";

                    textBlockSessionInfo.Text += "Login Succeedded";


                }
                catch (HttpRequestException hre)
                {
                    textBlockSessionInfo.Text += "Error:" + hre.Message;

                }
                catch (TaskCanceledException)
                {
                    textBlockSessionInfo.Text += "Request canceled.";

                }
                catch (Exception ex)
                {
                    textBlockSessionInfo.Text += ex.Message;

                }
                finally
                {
                    textBlockSessionInfo.Focus(FocusState.Programmatic);

                    this.buttonSubmit.IsEnabled = true;

                    if (httpClient != null)
                    {
                        httpClient.Dispose();
                        httpClient = null;
                    }
                }
            }
        }



        //Bring back the camera for another qr scanning
        private async void buttonVerifySession_Click(object sender, RoutedEventArgs e)
        {
            capturePreview.Visibility = Visibility.Visible;
            await camera.InitPreview(capturePreview);
            await camera.AutoFocus();
            timer.Start();

            textBlockSessionInfoExtra.Text = "";
        }



        //Toggle extra information
        private void buttonExpand_Click(object sender, RoutedEventArgs e)
        {
            if (gridExtraInfo.Visibility == Visibility.Collapsed)
                gridExtraInfo.Visibility = Visibility.Visible;
            else
                gridExtraInfo.Visibility = Visibility.Collapsed;
        }

        private async void capturePreview_Tapped(object sender, TappedRoutedEventArgs e)
        {
            await camera.AutoFocus();
        }
    }
}
