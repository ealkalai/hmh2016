using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EnterINGApp
{
    public class ResponseData
    {
        public string device { get; set; }
        public string user { get; set; }
        public string uuid { get; set; }

        public string service_id { get; set; }
        public string something_generic { get; set; }
        public string singedContract { get; set; }
    }

    public class QRCodeData
    {
        public string date ="";
        public string text="";
        public string uuid="";
        public string service_id="";
        public string something_generic="";
        //public string extra_parameters;
    }
}
