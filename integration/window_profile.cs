using System;
using System.Runtime.InteropServices;

// Chrome sets System.AppUserModel.ID for each window's profile.
namespace ChatSuccession
{
    public static class WindowProfile
    {
        private const ushort WideString = 31;  // VT_LPWSTR

        [StructLayout(LayoutKind.Sequential)]
        private struct PropertyKey
        {
            public Guid Format;
            public uint Id;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct PropertyValue
        {
            public ushort Type;
            public ushort Reserved1, Reserved2, Reserved3;
            public IntPtr Pointer, Padding;
        }

        [ComImport, Guid("886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99")]
        [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IPropertyStore
        {
            [PreserveSig] int GetCount(out uint count);
            [PreserveSig] int GetAt(uint index, out PropertyKey key);
            [PreserveSig] int GetValue(ref PropertyKey key, out PropertyValue value);
        }

        [DllImport("shell32.dll")]
        private static extern int SHGetPropertyStoreForWindow(
            IntPtr window, ref Guid iid, out IPropertyStore store);

        [DllImport("ole32.dll")]
        private static extern int PropVariantClear(ref PropertyValue value);

        public static string ReadAppId(IntPtr window)
        {
            Guid iid = typeof(IPropertyStore).GUID;
            IPropertyStore store;
            Marshal.ThrowExceptionForHR(SHGetPropertyStoreForWindow(window, ref iid, out store));
            try
            {
                var key = new PropertyKey
                {
                    Format = new Guid("9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3"),
                    Id = 5
                };
                PropertyValue value;
                Marshal.ThrowExceptionForHR(store.GetValue(ref key, out value));
                try
                {
                    return value.Type == WideString ? Marshal.PtrToStringUni(value.Pointer) : null;
                }
                finally { PropVariantClear(ref value); }
            }
            finally { Marshal.ReleaseComObject(store); }
        }
    }
}
