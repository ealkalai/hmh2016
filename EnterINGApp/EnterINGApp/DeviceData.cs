using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EnterINGApp
{
    public class DeviceData
    {
        public string DeviceId { get; set; }
        public string UserId { get; set; }
        private string HashedPIN { get; set; }

        public DeviceData(string device, string user, string hashedPin)
        {
            DeviceId = device; UserId = user; HashedPIN = hashedPin;
        }
        public bool ValidatePin(string hashedPin)
        {
            return HashedPIN == hashedPin;
        }


    }
}
