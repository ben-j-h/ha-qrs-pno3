# PNO3 Settings / Parameter Dictionary

Source: `GET /php/all_stream.php?js`  → defines JS global `qrs.vals`.
These `id`s are the `param=` values used with `changeSettings.php` / `changeSettingsJSON.php` `requestType=setParam|setQuickParam`, and the `id`s that appear in `all_stream.php` settings-delta entries `{id,val}`.

| id | default/current | range | description |
|---:|---|---|---|
| 0 | /dev/qrsmagnetics |  | SPI Device Path |
| 1 | 21 | 0-127 | Min PNOScan Note |
| 2 | 80 | 1-128 | Number of Notes |
| 3 | 0 | 0,1 | Notes Inverted |
| 4 | 0 | 0,1 | Magic Pedal |
| 5 | 25 | 0-127 | Lowest Note |
| 6 | 0 | -24-24 | Transpose PWM |
| 7 | 500 | 0-30000 | Note Delay (ms) |
| 8 | 50 | 0-500 | Density Compensation |
| 9 | 0 | 0,1 | Power Compensation Type |
| 10 | 80 | 0-200 | Power Compensation |
| 11 | 25 | 0-200 | Heat Compensation |
| 12 | 30 | 0-200 | Pedal Compensation |
| 13 | 16000 | 0-30000 | Max Note On Time (ms) |
| 14 | 20 | 0-255 | Absolute Min Force |
| 15 | 200 | 0-65535 | Min Rail Current Limit (ma) |
| 16 | 15001 | 0-65535 | Max Rail Current Limit (ma) |
| 17 | 550 | 0-65535 | Key Force Curve Shape |
| 18 | 22000 | 0-65535 | Max Pedal On Time (ms) |
| 19 | 0 | 0-5000 | Pedal Pre-Play Time (ms) |
| 20 | 16 | 1-128 | Max Simultaneous Notes |
| 21 | 120 | 0-5000 | Pedal Attack Time (ms) |
| 22 | 4300 | 0-10000 | Pedal Attack Percent (hundreths percent) |
| 23 | 2900 | 0-10000 | Pedal Hold Percent (hundreths percent) |
| 24 | 1 | 0-100 | Soft Volume |
| 25 | 50 | 0-100 | Dynamic Volume |
| 26 | 120 | 0-65535 | Pedal Retro Time (ms) |
| 27 | 1600 | 0-10000 | Pedal Retro Percent (hundreths percent) |
| 28 | 350 | 0-65535 | Min Pedal Current Limit (ma) |
| 29 | 8187 | 0-65535 | Max Pedal Current Limit (ma) |
| 30 | 1 | 0-100 | Remote Volume Increment |
| 31 | 50 | 0-100 | Piano Volume |
| 32 | 192.168.1.222 | 0.0.0.0-255.255.255.255 | Static IP |
| 33 | 255.255.255.0 | 0.0.0.0-255.255.255.255 | Subnet Mask |
| 34 | 192.168.0.225 | 0.0.0.0-255.255.255.255 | Gateway |
| 35 | 192.168.1.255 | 0.0.0.0-255.255.255.255 | Broadcast |
| 36 | 0 | 0-2 | Language |
| 37 | 0 | 0,1 | Recording |
| 38 | 0 | 0,1 | AutoSave Recordings |
| 39 | 2 | 0-127 | Adjust Active Note |
| 40 | 0 | 0,1 | Adjust Activated |
| 41 | 1 | 0-127 | Key Adjust Velocity |
| 42 | 1000 | 0,1 | Key Adjust On Time |
| 43 | 1000 | 0,1 | Key Adjust Off Time |
| 44 | QRSPNO3 |  | Hostname |
| 45 | 1 | 0-2 | Network Mode |
| 46 | 2 | 0-99 | Recording Timeout (sec) |
| 47 | 50 | 0-100 | Master Volume |
| 48 | 0 | -24-12 | EQ Band 0 |
| 49 | 0 | -24-12 | EQ Band 1 |
| 50 | 0 | -24-12 | EQ Band 2 |
| 54 | 0.12 |  | U-Boot Version |
| 55 | 4.19.37.4+ |  | Kernel Version |
| 56 | 0.661 |  | File System Version |
| 57 | 0.68 |  | Magnetics Version |
| 58 | 0 |  | Last Server DRM Timestamp |
| 59 | 1 | 0,1 | Check Updates |
| 60 | 100 | 0-65535 | Key Retro Time (ms) |
| 61 | 3 | 0-255 | Key Retro Divisor |
| 62 | 45123 |  | Pedal 1 Command |
| 63 | 45120 |  | Pedal 2 Command |
| 64 | 45122 |  | Pedal 3 Command |
| 65 | 192.168.2.22 | 0.0.0.0-255.255.255.255 | Static DNS 1 |
| 66 | 8.8.8.8 | 0.0.0.0-255.255.255.255 | Static DNS 2 |
| 67 | 0 | 0,1 | Plx Off |
| 68 | 0 | 0,1 | Stop metronome after first recorded note |
| 69 | 600 | 0-100000 | Idle Current Test Frequency (sec) |
| 70 | 2 | 0-3 | Current Testing Style ID |
| 71 | 1 | 0,1 | Test Current on Boot |
| 72 | 3 | 0-4 | Startup Play List Type |
| 73 | 1 |  | Startup Play List ID |
| 74 | 47 | 0,47 | Run CPU at 1GHz |
| 75 | /usr/factory/TimGM6mb.sf2 |  | Soundfont Path |
| 76 | Light | 0-4 | Theme |
| 77 | 0 | 0-100 | Audio Volume Curve Difference |
| 78 | 0 | 0-100 | Piano Volume Curve Difference |
| 79 | PNO30519009678 |  | Serial Number |
| 80 | 70 | 0-5000 | Key Min Off Time (ms) |
| 81 | 125 | 0-5000 | Pedal Min Off Time (ms) |
| 82 | 0 | 0,1 | Pre-Decompress MP3 |
| 83 | 1 | 0,1 | 5 Pin Midi Out |
| 84 | 0 | 0,1 | USB B Midi Out |
| 85 | 10 | 0-65535 | Playback Mode |
| 86 | 0 |  | Midi in Script Path |
| 87 | 0 |  | Aux in Script Path |
| 88 | 90000 | 0-1000000 | Demo Time (ms) |
| 89 | 1 | 0-5000 | Pedal Press Debounce (ms) |
| 90 | 2000 | 0-30000 | Power On Delay (ms) |
| 91 | 225 | 0-10000 | Stream Midi Delay (ms) |
| 92 | 300000 | 0-1000000 | Power Off Delay (ms) |
| 93 | 100 | 0-5000 | AMI Carrier Loss Count |
| 94 | America/Los_Angeles |  | Timezone |
| 95 | 195 | 0-10000 | Stream Audio Delay (ms) |
| 96 | 0 | 0-10000 | 5-Pin Midi In Delay to PWM (ms) |
| 97 | 0 | 0-10000 | USB B Midi In Delay to PWM (ms) |
| 98 | 1 | 0,1 | Apply MIDI Out Volume Curve to Velocities |
| 99 | 0 | 0-65535 | MIDI Out Volume Command Channel Mask |
| 100 | 0 | 0,1 | Apply MIDI Out Minimum Velocities |
| 101 | 80 | 1-128 | Number of MIDI Out Notes |
| 102 | 25 | 0-127 | Lowest MIDI Out Note |
| 103 | 4000 | 0-65535 | Max Current Per Full Force Key (mA) |
| 104 | 7000 | 0-65535 | Key Overcurrent Timeout (ms) |
| 105 | 5450 | 0-65535 | Max Current Per Full Force Pedal (mA) |
| 106 | 5000 | 0-65535 | Pedal Overcurrent Timeout (ms) |
| 107 | /dev/ttyO3 |  | Smart Driver Device Path |
| 108 | 4255 |  | Media Verification Current Position |
| 109 | 0 | 1-255 | Highest Driver Board Address |
| 110 | 1 | 0-1 | Magnetics Key Drive Enabled |
| 111 | 0.29 |  | Smart Driver Version |
| 112 | 1 | 0,1 | Play Recordings With Synth |
| 113 | 0 | 0,1 | Record With Synth |
| 114 | 0 | 0,1 | Synth Out 3(Lower Left) |
| 115 | 0 | 0,1 | Playback Files with Synth Sound |
| 116 | 0 | 0,1 | QRS-Connect Auto Upload |
| 117 | 0 | ? | QRS-Connect Successful Login |
| 118 | 256 | 0-32768 | ADC Slow Filter Divisor |
| 119 | 150 | 0-32768 | Adjust Time (ms) |
| 120 | 5 | 0-32768 | Key Min On Time (ms) |
| 121 | 16 | 0-32768 | ADC Fast Filter Divisor |
| 122 | /usr/factory/TimGM6mb.sf2 |  | Default Soundfont |
| 123 | 0 | 0,1 | Always Recording |
| 124 | 0 | 0-10000 | Synth Delay |
| 125 | 500 | 0-10000 | 5-pin Midi Out Delay(ms) |
| 126 | 0 | 0-10000 | USB B Midi Out Delay(ms) |
| 127 | 1 | 0,1 | Synth Out 2(Upper Right) |
| 128 | 0 | 0,1 | Synth Out 4(Lower Right) |
| 129 | 0 | 0,1 | PNO Practice Toggle |
| 130 |  |  | PNO Name |
| 131 | 0 | 0,1 | Local Video Server |
| 132 | 0 | 0,1 | Edit Low Modulation |
| 133 | 1 | 0,1 | PNOscan to 5-Pin Midi Out |
| 134 | 0 | 0,1 | PNOscan to USB B Midi Out |
| 135 | 0 | 0,1 | PNOscan to PWM |
| 136 | 0 | 0,1 | Allow Remote Server Changes |
| 137 | 300 | 0-5000 | Min. Note Delay Force Comp(ms) |
| 138 | 1 | 0-5000 | Min PNOScan Pedal Off Time (ms) |
| 139 | 10800 | 0-50000 | Expected Solenoid Resistance (mOhm) |
| 140 | 3800 | 0-50000 | Min Solenoid Resistance (mOhm) |
| 142 | 33 | 0-127 | Metronome Weak Note |
| 143 | 34 | 0-127 | Metronome Strong Note |
| 144 | 9 | 1-16 | Metronome Synth Channel |
| 145 | 0 | 0-4 | Audio in AMI Source |
| 146 | 0 | 0-4 | Calliope |
| 147 | 0 | 0,1 | USB B to PWM |
| 148 | 1 | 0,1 | 5-Pin MIDI in to PWM |
| 149 | 9 | 0-23 | Update Hour |
| 150 | 1 | 0,1 | WiFi Installed |
| 151 | 1 | 0-3 | WiFi Mode |
| 152 | QRSPNO3_09678 |  | WiFi AP SSID |
| 153 | U2FsdGVkX19VaK6zyOyWvwdhAxXUGlaoAIPzGB6Wvvk= |  | WiFi AP Passphrase |
| 154 | 192.168.1.222 | 0.0.0.0-255.255.255.255 | WiFi IP Address |
| 155 | 255.255.255.0 | 0.0.0.0-255.255.255.255 | WiFi Subnet Mask |
| 156 | 192.168.1.1 | 0.0.0.0-255.255.255.255 | WiFi Gateway |
| 157 | 192.168.1.255 | 0.0.0.0-255.255.255.255 | WiFi Broadcast |
| 158 | 4.2.2.1 | 0.0.0.0-255.255.255.255 | WiFi Primary DNS |
| 159 | 8.8.8.8 | 0.0.0.0-255.255.255.255 | WiFi Secondary DNS |
| 160 | -1 | 0-127 | Synth Channel Volume 1 |
| 161 | -1 | 0-127 | Synth Channel Volume 2 |
| 162 | -1 | 0-127 | Synth Channel Volume 3 |
| 163 | -1 | 0-127 | Synth Channel Volume 4 |
| 164 | -1 | 0-127 | Synth Channel Volume 5 |
| 165 | -1 | 0-127 | Synth Channel Volume 6 |
| 166 | -1 | 0-127 | Synth Channel Volume 7 |
| 167 | -1 | 0-127 | Synth Channel Volume 8 |
| 168 | -1 | 0-127 | Synth Channel Volume 9 |
| 169 | -1 | 0-127 | Synth Channel Volume 10 |
| 170 | -1 | 0-127 | Synth Channel Volume 11 |
| 171 | -1 | 0-127 | Synth Channel Volume 12 |
| 172 | -1 | 0-127 | Synth Channel Volume 13 |
| 173 | -1 | 0-127 | Synth Channel Volume 14 |
| 174 | -1 | 0-127 | Synth Channel Volume 15 |
| 175 | -1 | 0-127 | Synth Channel Volume 16 |
| 176 | 20 | 0-23 | Hour To Start Muting Prompts |
| 177 | -1 | -1-24 | Duration of Hours to Mute Prompts |
| 178 | 0 | 0,1 | Nickelodeon |
| 179 | 0 | 0,1 | 5 Pin In to 5 Pin Out |
| 180 |  |  | Alexa Activation |
| 182 | 8.8.8.8 | 0.0.0.0-255.255.255.255 | Internet Check IP |
| 183 | 0 | 0,1 | Disable Online Checks |
| 184 | 0 | 0-1 | Bluetooth Enabled |
| 185 | 0 | 0-1 | WiFi AP Enabled |
| 186 | 10.3.2.1 | 0.0.0.0-255.255.255.255 | WiFi AP IP Address |
| 187 | 255.255.255.0 | 0.0.0.0-255.255.255.255 | WiFi AP Subnet Mask |
| 188 | 8.8.8.8	8.8.4.4 | 0.0.0.0-255.255.255.255 | WiFi AP DNS Server List |
| 189 | 10.3.2.10 | 0.0.0.0-255.255.255.255 | WiFi AP DHCP Start Address |
| 190 | 10.3.2.100 | 0.0.0.0-255.255.255.255 | WiFi AP DHCP Stop Address |
| 191 | 11 | 0-11 | WiFi AP Channel |
| 192 | 129 | 0-255 | Bluetooth MIDI Client |
| 193 | 0 | 0-255 | Bluetooth MIDI Port |
| 194 | 0 | 0-10000 | Bluetooth Audio In Delay (ms) |
| 195 | 0 | 0-10000 | Bluetooth AMI In MIDI Delay (ms) |
| 196 | 0 | 0-4 | Bluetooth In AMI Source |
| 197 | 0 | 0-2 | Rail Mount Type |
| 198 | 10.0.10.2 | 0.0.0.0-255.255.255.255 | Video Server Address |
| 199 | /media/microsdp1 |  | System Library Path |
| 200 | 1 | 0-127 | Note 0 Min MIDI Out Velocity |
| 201 | 1 | 0-127 | Note 1 Min MIDI Out Velocity |
| 202 | 1 | 0-127 | Note 2 Min MIDI Out Velocity |
| 203 | 1 | 0-127 | Note 3 Min MIDI Out Velocity |
| 204 | 1 | 0-127 | Note 4 Min MIDI Out Velocity |
| 205 | 1 | 0-127 | Note 5 Min MIDI Out Velocity |
| 206 | 1 | 0-127 | Note 6 Min MIDI Out Velocity |
| 207 | 1 | 0-127 | Note 7 Min MIDI Out Velocity |
| 208 | 1 | 0-127 | Note 8 Min MIDI Out Velocity |
| 209 | 1 | 0-127 | Note 9 Min MIDI Out Velocity |
| 210 | 1 | 0-127 | Note 10 Min MIDI Out Velocity |
| 211 | 1 | 0-127 | Note 11 Min MIDI Out Velocity |
| 212 | 1 | 0-127 | Note 12 Min MIDI Out Velocity |
| 213 | 1 | 0-127 | Note 13 Min MIDI Out Velocity |
| 214 | 1 | 0-127 | Note 14 Min MIDI Out Velocity |
| 215 | 1 | 0-127 | Note 15 Min MIDI Out Velocity |
| 216 | 1 | 0-127 | Note 16 Min MIDI Out Velocity |
| 217 | 1 | 0-127 | Note 17 Min MIDI Out Velocity |
| 218 | 1 | 0-127 | Note 18 Min MIDI Out Velocity |
| 219 | 1 | 0-127 | Note 19 Min MIDI Out Velocity |
| 220 | 1 | 0-127 | Note 20 Min MIDI Out Velocity |
| 221 | 1 | 0-127 | Note 21 Min MIDI Out Velocity |
| 222 | 1 | 0-127 | Note 22 Min MIDI Out Velocity |
| 223 | 1 | 0-127 | Note 23 Min MIDI Out Velocity |
| 224 | 1 | 0-127 | Note 24 Min MIDI Out Velocity |
| 225 | 1 | 0-127 | Note 25 Min MIDI Out Velocity |
| 226 | 1 | 0-127 | Note 26 Min MIDI Out Velocity |
| 227 | 1 | 0-127 | Note 27 Min MIDI Out Velocity |
| 228 | 1 | 0-127 | Note 28 Min MIDI Out Velocity |
| 229 | 1 | 0-127 | Note 29 Min MIDI Out Velocity |
| 230 | 1 | 0-127 | Note 30 Min MIDI Out Velocity |
| 231 | 1 | 0-127 | Note 31 Min MIDI Out Velocity |
| 232 | 1 | 0-127 | Note 32 Min MIDI Out Velocity |
| 233 | 1 | 0-127 | Note 33 Min MIDI Out Velocity |
| 234 | 1 | 0-127 | Note 34 Min MIDI Out Velocity |
| 235 | 1 | 0-127 | Note 35 Min MIDI Out Velocity |
| 236 | 1 | 0-127 | Note 36 Min MIDI Out Velocity |
| 237 | 1 | 0-127 | Note 37 Min MIDI Out Velocity |
| 238 | 1 | 0-127 | Note 38 Min MIDI Out Velocity |
| 239 | 1 | 0-127 | Note 39 Min MIDI Out Velocity |
| 240 | 1 | 0-127 | Note 40 Min MIDI Out Velocity |
| 241 | 1 | 0-127 | Note 41 Min MIDI Out Velocity |
| 242 | 1 | 0-127 | Note 42 Min MIDI Out Velocity |
| 243 | 1 | 0-127 | Note 43 Min MIDI Out Velocity |
| 244 | 1 | 0-127 | Note 44 Min MIDI Out Velocity |
| 245 | 1 | 0-127 | Note 45 Min MIDI Out Velocity |
| 246 | 1 | 0-127 | Note 46 Min MIDI Out Velocity |
| 247 | 1 | 0-127 | Note 47 Min MIDI Out Velocity |
| 248 | 1 | 0-127 | Note 48 Min MIDI Out Velocity |
| 249 | 1 | 0-127 | Note 49 Min MIDI Out Velocity |
| 250 | 1 | 0-127 | Note 50 Min MIDI Out Velocity |
| 251 | 1 | 0-127 | Note 51 Min MIDI Out Velocity |
| 252 | 1 | 0-127 | Note 52 Min MIDI Out Velocity |
| 253 | 1 | 0-127 | Note 53 Min MIDI Out Velocity |
| 254 | 1 | 0-127 | Note 54 Min MIDI Out Velocity |
| 255 | 1 | 0-127 | Note 55 Min MIDI Out Velocity |
| 256 | 1 | 0-127 | Note 56 Min MIDI Out Velocity |
| 257 | 1 | 0-127 | Note 57 Min MIDI Out Velocity |
| 258 | 1 | 0-127 | Note 58 Min MIDI Out Velocity |
| 259 | 1 | 0-127 | Note 59 Min MIDI Out Velocity |
| 260 | 1 | 0-127 | Note 60 Min MIDI Out Velocity |
| 261 | 1 | 0-127 | Note 61 Min MIDI Out Velocity |
| 262 | 1 | 0-127 | Note 62 Min MIDI Out Velocity |
| 263 | 1 | 0-127 | Note 63 Min MIDI Out Velocity |
| 264 | 1 | 0-127 | Note 64 Min MIDI Out Velocity |
| 265 | 1 | 0-127 | Note 65 Min MIDI Out Velocity |
| 266 | 1 | 0-127 | Note 66 Min MIDI Out Velocity |
| 267 | 1 | 0-127 | Note 67 Min MIDI Out Velocity |
| 268 | 1 | 0-127 | Note 68 Min MIDI Out Velocity |
| 269 | 1 | 0-127 | Note 69 Min MIDI Out Velocity |
| 270 | 1 | 0-127 | Note 70 Min MIDI Out Velocity |
| 271 | 1 | 0-127 | Note 71 Min MIDI Out Velocity |
| 272 | 1 | 0-127 | Note 72 Min MIDI Out Velocity |
| 273 | 1 | 0-127 | Note 73 Min MIDI Out Velocity |
| 274 | 1 | 0-127 | Note 74 Min MIDI Out Velocity |
| 275 | 1 | 0-127 | Note 75 Min MIDI Out Velocity |
| 276 | 1 | 0-127 | Note 76 Min MIDI Out Velocity |
| 277 | 1 | 0-127 | Note 77 Min MIDI Out Velocity |
| 278 | 1 | 0-127 | Note 78 Min MIDI Out Velocity |
| 279 | 1 | 0-127 | Note 79 Min MIDI Out Velocity |
| 280 | 1 | 0-127 | Note 80 Min MIDI Out Velocity |
| 281 | 1 | 0-127 | Note 81 Min MIDI Out Velocity |
| 282 | 1 | 0-127 | Note 82 Min MIDI Out Velocity |
| 283 | 1 | 0-127 | Note 83 Min MIDI Out Velocity |
| 284 | 1 | 0-127 | Note 84 Min MIDI Out Velocity |
| 285 | 1 | 0-127 | Note 85 Min MIDI Out Velocity |
| 286 | 1 | 0-127 | Note 86 Min MIDI Out Velocity |
| 287 | 1 | 0-127 | Note 87 Min MIDI Out Velocity |
| 288 | 1 | 0-127 | Note 88 Min MIDI Out Velocity |
| 289 | 1 | 0-127 | Note 89 Min MIDI Out Velocity |
| 290 | 1 | 0-127 | Note 90 Min MIDI Out Velocity |
| 291 | 1 | 0-127 | Note 91 Min MIDI Out Velocity |
| 292 | 1 | 0-127 | Note 92 Min MIDI Out Velocity |
| 293 | 1 | 0-127 | Note 93 Min MIDI Out Velocity |
| 294 | 1 | 0-127 | Note 94 Min MIDI Out Velocity |
| 295 | 1 | 0-127 | Note 95 Min MIDI Out Velocity |
| 296 | 1 | 0-127 | Note 96 Min MIDI Out Velocity |
| 297 | 1 | 0-127 | Note 97 Min MIDI Out Velocity |
| 298 | 1 | 0-127 | Note 98 Min MIDI Out Velocity |
| 299 | 1 | 0-127 | Note 99 Min MIDI Out Velocity |
| 300 | 1 | 0-127 | Note 100 Min MIDI Out Velocity |
| 301 | 1 | 0-127 | Note 101 Min MIDI Out Velocity |
| 302 | 1 | 0-127 | Note 102 Min MIDI Out Velocity |
| 303 | 1 | 0-127 | Note 103 Min MIDI Out Velocity |
| 304 | 1 | 0-127 | Note 104 Min MIDI Out Velocity |
| 305 | 1 | 0-127 | Note 105 Min MIDI Out Velocity |
| 306 | 1 | 0-127 | Note 106 Min MIDI Out Velocity |
| 307 | 1 | 0-127 | Note 107 Min MIDI Out Velocity |
| 308 | 1 | 0-127 | Note 108 Min MIDI Out Velocity |
| 309 | 1 | 0-127 | Note 109 Min MIDI Out Velocity |
| 310 | 1 | 0-127 | Note 110 Min MIDI Out Velocity |
| 311 | 1 | 0-127 | Note 111 Min MIDI Out Velocity |
| 312 | 1 | 0-127 | Note 112 Min MIDI Out Velocity |
| 313 | 1 | 0-127 | Note 113 Min MIDI Out Velocity |
| 314 | 1 | 0-127 | Note 114 Min MIDI Out Velocity |
| 315 | 1 | 0-127 | Note 115 Min MIDI Out Velocity |
| 316 | 1 | 0-127 | Note 116 Min MIDI Out Velocity |
| 317 | 1 | 0-127 | Note 117 Min MIDI Out Velocity |
| 318 | 1 | 0-127 | Note 118 Min MIDI Out Velocity |
| 319 | 1 | 0-127 | Note 119 Min MIDI Out Velocity |
| 320 | 1 | 0-127 | Note 120 Min MIDI Out Velocity |
| 321 | 1 | 0-127 | Note 121 Min MIDI Out Velocity |
| 322 | 1 | 0-127 | Note 122 Min MIDI Out Velocity |
| 323 | 1 | 0-127 | Note 123 Min MIDI Out Velocity |
| 324 | 1 | 0-127 | Note 124 Min MIDI Out Velocity |
| 325 | 1 | 0-127 | Note 125 Min MIDI Out Velocity |
| 326 | 1 | 0-127 | Note 126 Min MIDI Out Velocity |
| 327 | 1 | 0-127 | Note 127 Min MIDI Out Velocity |
| 330 | 0 | 0,1 | PNOScan to Bluetooth MIDI |
| 331 | 0 | 0,1 | Bluetooth MIDI to PWM |
| 332 | 0 | 0,1 | Bluetooth MIDI Out |
| 333 | 0 | 0-10000 | Bluetooth MIDI Out Delay(ms) |
| 334 | 0 | 0,1 | Bluetooth MIDI to 5Pin MIDI |
| 335 | 0 | 0,1 | Bluetooth MIDI to USB B MIDI |
| 336 | 0 | 0-10000 | Audio Out 3 Delay(ms) |
| 337 | 0 | 0-10000 | Audio Out 4 Delay(ms) |
| 338 | 0 | 0-10000 | Audio Out 1 Delay(ms) |
| 339 | 0 | 0-10000 | Bluetooth Audio Out Delay(ms) |
| 340 | qrspno.net |  | SSH Server Path |
| 341 | root |  | SSH Username |
| 342 | U2FsdGVkX1+cD1DebkQicNKI6DyAZGJmE4PAtoL0zI0= |  | SSH Password |
| 343 | /PMIII/LIBRARY |  | SSH Library Path |
| 344 | 0 | 0-65535 | MIDI Out Individual off Mask |
| 345 | 7 | 0-7 | Network Prompt Mask |
| 346 | 5000 | 0-65535 | Record PPQN |
| 347 | 1 | 0-1 | PLX Volume |
| 348 | 5 | -1-99 | Splash Screen |
| 349 | 0 | 0-2 | Run fsck next boot |
| 350 | 0 | 0-2 | Coin-Op Enable |
| 351 | 1 | 0.1-10 | Credits per Pulse |
| 352 | 0 | 0-10 | Number of Credits |
| 353 | 0 | 0-1 | USB Logging |
| 354 | -1 | -1-999999999999999999 | ABI Epoch Time |
| 355 | 0 | 0-999999999999999999 | ABI Last Total Reps |
| 356 | 0 | 0-999999999999999999 | ABI Last Total Notes |
| 357 | 0 | 0-999999999999999999 | ABI Cumulative Reps |
| 358 | 0 | 0-999999999999999999 | ABI Cumulative Notes |
| 359 | 0 | 0-1 | ABI Status |
| 360 | 0 | 0-1 | Studio Preset Overlay Enabled |
| 361 | 0 | 0-1 | Alt Standalone IP |
| 362 | 0 | 0-1 | External Violin |
| 363 | 39 | 0-255 | USB MIDI Device 1 Client |
| 364 | 19 | 0-255 | USB MIDI Device 1 Port |
| 365 | 0 | 0-255 | USB MIDI Device 2 Client |
| 366 | 0 | 0-255 | USB MIDI Device 2 Port |
| 367 | 0 | 0,1 | USBA1 to PWM |
| 368 | 0 | 0,1 | USBA1 to 5Pin Out |
| 369 | 0 | 0,1 | USBA1 to Bluetooth Out |
| 370 | 0 | 0,1 | USBA1 to USBA2 |
| 371 | 0 | 0,1 | USBA1 to USBB |
| 372 | 0 | 0,1 | 5Pin to USBA |
| 373 | 0 | 0,1 | PNOscan to USBA |
| 374 | 0 | 0,1 | Bluetooth to USBA |
| 375 | 0 | 0,1 | USBA1 MIDI Out |
| 376 | 500 | 0-10000 | USBA1 MIDI Out Delay(ms) |
| 377 | 0 | 0,1 | USBA2 to PWM |
| 378 | 0 | 0,1 | USBA2 to 5Pin Out |
| 379 | 0 | 0,1 | USBA2 to Bluetooth Out |
| 380 | 0 | 0,1 | USBA2 to USBA1 |
| 381 | 0 | 0,1 | USBA2 to USBB |
| 382 | 0 | 0,1 | 5Pin to USBB |
| 383 | 0 | 0,1 | PNOscan to USBB |
| 384 | 0 | 0,1 | Bluetooth to USBB |
| 385 | 0 | 0,1 | USBA2 MIDI Out |
| 386 | 0 | 0-10000 | USBA2 MIDI Out Delay(ms) |
| 387 |  |  | Google Activation |
| 388 |  |  | Google Token |
| 389 | 10 | -20-19 | Lighttpd Nice Level |
| 390 | 1 | 0-1 | Controller 7 Volume Control |
| 391 | 360 | -1-9999 | SSH Update Auto Check Time (min) |
| 392 | PNO |  | SSH Username |
| 393 | U2FsdGVkX19RHNbTISsOsWrSdeNKY52c6lohX5mLz9Mi4iCUmbDAhGcqr6aXBai5 |  | SSH Password |
| 394 | update.qrspno.com |  | SSH Server |
| 395 | 0.661 |  | SSH Version Available |
| 396 | -1 | -1-9999 | SSH Media Auto Check Time (min) |
| 397 |  |  | SSH Media Version Available |
| 398 | 16 | 1-32 | Fluidsynth Polyphony |
| 399 | 0 | 0,1 | Update Auto-Check use Rsync |
| 400 | 0 | 0,1 | Update Media-Check use Rsync |
| 401 | 1 | 0,1 | Use Rsync |
| 402 | 1 | 0,1 | MIDI Player System |
| 403 | 1 | 0-127 | MIDI Out Pedal Min |
| 404 | 127 | 0-127 | MIDI Out Pedal Max |
| 405 | 5000 | 100-10000 | Pedal Test On Time |
| 406 | pno3mqtt.qrs-connect.com:1883 | 0.0.0.0-255.255.255.255 | QRS Server IP |
| 407 | admin |  | Mosquitto Local User |
| 408 | U2FsdGVkX18JcjAiZS4Yg6tvckfV64PGusI+g/NoP8E= |  | Mosquitto Local Pass |
| 409 | qrs |  | QRS Server User |
| 410 | U2FsdGVkX1+e9ELPQlN9AdRE5H6g9u6O9C+OozqOCek= |  | QRS Server Pass |
| 411 | 500 | 500-65535 | MQTT On disconnect delay |
| 412 | 150 | 1-1000000 | MQTT Bucket Delay (mS) |
| 413 | 500000 | 1-999999999 | MIDI Mosquitto Delay |
| 414 | 0 | 0-2 | MIDI_MQTT_QOS |
| 415 | 0 | 0-1 | MQTT Use Real-time |
| 416 | 1 | 0,1 | QRS-Connect to Piano |
| 417 | 1 | 0,1 | QRS-Connect to 5 Pin |
| 418 | 0 | 0,1 | QRS-Connect to USB B |
| 419 | 0 | 0,1 | QRS-Connect to USB A1 |
| 420 | 0 | 0,1 | QRS-Connect to USB A2 |
| 421 | 0 | 0,1 | QRS-Connect to Bt |
| 422 | 0 | 0,1 | File to QRS-Connect |
| 423 | 0 | 0,1 | PNOscan to QRS-Connect |
| 424 | 0 | 0,1 | 5 Pin to QRS-Connect |
| 425 | 0 | 0,1 | USB Client to QRS-Connect |
| 426 | 0 | 0,1 | USB Host 1 to QRS-Connect |
| 427 | 0 | 0,1 | USB Host 2 to QRS-Connect |
| 428 | 0 | 0,1 | File to Local MQTT |
| 429 | 0 | 0,1 | PNOscan to Local MQTT |
| 430 | 0 | 0,1 | 5 Pin to Local MQTT |
| 431 | 0 | 0,1 | USB Client to Local MQTT |
| 432 | 0 | 0,1 | USB Host 1 to Local MQTT |
| 433 | 0 | 0,1 | USB Host 2 to Local MQTT |
| 434 | 1 | 0-1 | Media Rsync use daemon |
| 435 | 15 | -20-20 | RSync Nice Level |
| 436 | 125 | 0-30000 | MQQT Override Note Delay (ms) |
| 437 | 500 | 0-30000 | MQQT Active Timeout (ms) |
| 438 | 120000 | 0-600000 | Manual Power Hold Time (ms) |
| 439 |  |  | Radio Preset 1 |
| 440 |  |  | Radio Preset 2 |
| 441 |  |  | Radio Preset 3 |
| 442 | 0 | 0-1 | Synth Plays on Solo Midi Only |
| 443 | 0 | 0-1 | Show EQ |
| 444 | 0 | 0-99999 | AMI Reset Time (min) |
| 445 | 0 | 0-1 | ABI File Select |
| 446 | 0 | 0-1 | Show CPU Info |
| 447 | 1 | 0-1 | Enable Third Party API |
| 448 | 0 | 0-999999 | Third Party Code |
| 449 | 0 | 0-1 | Enable Standard Bluetooth |
| 450 |  | 0.0.0.0-255.255.255.255 | Roku IP |
| 451 | none | debug,error,warning,notice,information,subscribe,unsubscribe,websockets,none,all | MQTT Log Types |
| 452 | 0 | 0,60-999999 | Routine Kill Time (sec) |
| 453 | 8600,8750,9750 |  | Allowed Synth Prefixes |
| 454 | 0 | 0-4 | Trumpet Output |
| 500 | 75 | 0-376 | Key 0 On Force |
| 501 | 0 | 0-255 | Key 0 Force Curve ID |
| 502 | 376 | 0-376 | Key 0 Max Force |
| 503 | 3 | 1-255 | Key 0 Retro Divisor |
| 504 | 100 | 0-65535 | Key 0 Retro Time(ms) |
| 505 | 0 | 0-30000 | Key 0 Max On Time(ms) |
| 525 | 65 | 0-376 | Key 96 On Force |
| 526 | 0 | 0-255 | Key 96 Force Curve ID |
| 527 | 376 | 0-376 | Key 96 Max Force |
| 528 | 3 | 1-255 | Key 96 Retro Divisor |
| 529 | 100 | 0-65535 | Key 96 Retro Time(ms) |
| 530 | 0 | 0-30000 | Key 96 Max On Time(ms) |
| 550 | 84 | 0-376 | Key 1 On Force |
| 551 | 0 | 0-255 | Key 1 Force Curve ID |
| 552 | 376 | 0-376 | Key 1 Max Force |
| 553 | 3 | 1-255 | Key 1 Retro Divisor |
| 554 | 100 | 0-65535 | Key 1 Retro Time(ms) |
| 555 | 0 | 0-30000 | Key 1 Max On Time(ms) |
| 575 | 65 | 0-376 | Key 97 On Force |
| 576 | 0 | 0-255 | Key 97 Force Curve ID |
| 577 | 376 | 0-376 | Key 97 Max Force |
| 578 | 3 | 1-255 | Key 97 Retro Divisor |
| 579 | 100 | 0-65535 | Key 97 Retro Time(ms) |
| 580 | 0 | 0-30000 | Key 97 Max On Time(ms) |
| 600 | 76 | 0-376 | Key 2 On Force |
| 601 | 0 | 0-255 | Key 2 Force Curve ID |
| 602 | 376 | 0-376 | Key 2 Max Force |
| 603 | 3 | 1-255 | Key 2 Retro Divisor |
| 604 | 100 | 0-65535 | Key 2 Retro Time(ms) |
| 605 | 0 | 0-30000 | Key 2 Max On Time(ms) |
| 625 | 65 | 0-376 | Key 98 On Force |
| 626 | 0 | 0-255 | Key 98 Force Curve ID |
| 627 | 376 | 0-376 | Key 98 Max Force |
| 628 | 3 | 1-255 | Key 98 Retro Divisor |
| 629 | 100 | 0-65535 | Key 98 Retro Time(ms) |
| 630 | 0 | 0-30000 | Key 98 Max On Time(ms) |
| 650 | 69 | 0-376 | Key 3 On Force |
| 651 | 0 | 0-255 | Key 3 Force Curve ID |
| 652 | 376 | 0-376 | Key 3 Max Force |
| 653 | 3 | 1-255 | Key 3 Retro Divisor |
| 654 | 100 | 0-65535 | Key 3 Retro Time(ms) |
| 655 | 0 | 0-30000 | Key 3 Max On Time(ms) |
| 675 | 65 | 0-376 | Key 99 On Force |
| 676 | 0 | 0-255 | Key 99 Force Curve ID |
| 677 | 376 | 0-376 | Key 99 Max Force |
| 678 | 3 | 1-255 | Key 99 Retro Divisor |
| 679 | 100 | 0-65535 | Key 99 Retro Time(ms) |
| 680 | 0 | 0-30000 | Key 99 Max On Time(ms) |
| 700 | 76 | 0-376 | Key 4 On Force |
| 701 | 0 | 0-255 | Key 4 Force Curve ID |
| 702 | 376 | 0-376 | Key 4 Max Force |
| 703 | 3 | 1-255 | Key 4 Retro Divisor |
| 704 | 100 | 0-65535 | Key 4 Retro Time(ms) |
| 705 | 0 | 0-30000 | Key 4 Max On Time(ms) |
| 725 | 65 | 0-376 | Key 100 On Force |
| 726 | 0 | 0-255 | Key 100 Force Curve ID |
| 727 | 376 | 0-376 | Key 100 Max Force |
| 728 | 3 | 1-255 | Key 100 Retro Divisor |
| 729 | 100 | 0-65535 | Key 100 Retro Time(ms) |
| 730 | 0 | 0-30000 | Key 100 Max On Time(ms) |
| 750 | 75 | 0-376 | Key 5 On Force |
| 751 | 0 | 0-255 | Key 5 Force Curve ID |
| 752 | 376 | 0-376 | Key 5 Max Force |
| 753 | 3 | 1-255 | Key 5 Retro Divisor |
| 754 | 100 | 0-65535 | Key 5 Retro Time(ms) |
| 755 | 0 | 0-30000 | Key 5 Max On Time(ms) |
| 775 | 65 | 0-376 | Key 101 On Force |
| 776 | 0 | 0-255 | Key 101 Force Curve ID |
| 777 | 376 | 0-376 | Key 101 Max Force |
| 778 | 3 | 1-255 | Key 101 Retro Divisor |
| 779 | 100 | 0-65535 | Key 101 Retro Time(ms) |
| 780 | 0 | 0-30000 | Key 101 Max On Time(ms) |
| 800 | 77 | 0-376 | Key 6 On Force |
| 801 | 0 | 0-255 | Key 6 Force Curve ID |
| 802 | 376 | 0-376 | Key 6 Max Force |
| 803 | 3 | 1-255 | Key 6 Retro Divisor |
| 804 | 100 | 0-65535 | Key 6 Retro Time(ms) |
| 805 | 0 | 0-30000 | Key 6 Max On Time(ms) |
| 825 | 65 | 0-376 | Key 102 On Force |
| 826 | 0 | 0-255 | Key 102 Force Curve ID |
| 827 | 376 | 0-376 | Key 102 Max Force |
| 828 | 3 | 1-255 | Key 102 Retro Divisor |
| 829 | 100 | 0-65535 | Key 102 Retro Time(ms) |
| 830 | 0 | 0-30000 | Key 102 Max On Time(ms) |
| 850 | 72 | 0-376 | Key 7 On Force |
| 851 | 0 | 0-255 | Key 7 Force Curve ID |
| 852 | 376 | 0-376 | Key 7 Max Force |
| 853 | 3 | 1-255 | Key 7 Retro Divisor |
| 854 | 100 | 0-65535 | Key 7 Retro Time(ms) |
| 855 | 0 | 0-30000 | Key 7 Max On Time(ms) |
| 875 | 65 | 0-376 | Key 103 On Force |
| 876 | 0 | 0-255 | Key 103 Force Curve ID |
| 877 | 376 | 0-376 | Key 103 Max Force |
| 878 | 3 | 1-255 | Key 103 Retro Divisor |
| 879 | 100 | 0-65535 | Key 103 Retro Time(ms) |
| 880 | 0 | 0-30000 | Key 103 Max On Time(ms) |
| 900 | 71 | 0-376 | Key 8 On Force |
| 901 | 0 | 0-255 | Key 8 Force Curve ID |
| 902 | 376 | 0-376 | Key 8 Max Force |
| 903 | 3 | 1-255 | Key 8 Retro Divisor |
| 904 | 100 | 0-65535 | Key 8 Retro Time(ms) |
| 905 | 0 | 0-30000 | Key 8 Max On Time(ms) |
| 925 | 65 | 0-376 | Key 104 On Force |
| 926 | 0 | 0-255 | Key 104 Force Curve ID |
| 927 | 376 | 0-376 | Key 104 Max Force |
| 928 | 3 | 1-255 | Key 104 Retro Divisor |
| 929 | 100 | 0-65535 | Key 104 Retro Time(ms) |
| 930 | 0 | 0-30000 | Key 104 Max On Time(ms) |
| 950 | 67 | 0-376 | Key 9 On Force |
| 951 | 0 | 0-255 | Key 9 Force Curve ID |
| 952 | 376 | 0-376 | Key 9 Max Force |
| 953 | 3 | 1-255 | Key 9 Retro Divisor |
| 954 | 100 | 0-65535 | Key 9 Retro Time(ms) |
| 955 | 0 | 0-30000 | Key 9 Max On Time(ms) |
| 975 | 65 | 0-376 | Key 105 On Force |
| 976 | 0 | 0-255 | Key 105 Force Curve ID |
| 977 | 376 | 0-376 | Key 105 Max Force |
| 978 | 3 | 1-255 | Key 105 Retro Divisor |
| 979 | 100 | 0-65535 | Key 105 Retro Time(ms) |
| 980 | 0 | 0-30000 | Key 105 Max On Time(ms) |
| 1000 | 68 | 0-376 | Key 10 On Force |
| 1001 | 0 | 0-255 | Key 10 Force Curve ID |
| 1002 | 376 | 0-376 | Key 10 Max Force |
| 1003 | 3 | 1-255 | Key 10 Retro Divisor |
| 1004 | 100 | 0-65535 | Key 10 Retro Time(ms) |
| 1005 | 0 | 0-30000 | Key 10 Max On Time(ms) |
| 1025 | 65 | 0-376 | Key 106 On Force |
| 1026 | 0 | 0-255 | Key 106 Force Curve ID |
| 1027 | 376 | 0-376 | Key 106 Max Force |
| 1028 | 3 | 1-255 | Key 106 Retro Divisor |
| 1029 | 100 | 0-65535 | Key 106 Retro Time(ms) |
| 1030 | 0 | 0-30000 | Key 106 Max On Time(ms) |
| 1050 | 68 | 0-376 | Key 11 On Force |
| 1051 | 0 | 0-255 | Key 11 Force Curve ID |
| 1052 | 376 | 0-376 | Key 11 Max Force |
| 1053 | 3 | 1-255 | Key 11 Retro Divisor |
| 1054 | 100 | 0-65535 | Key 11 Retro Time(ms) |
| 1055 | 0 | 0-30000 | Key 11 Max On Time(ms) |
| 1075 | 65 | 0-376 | Key 107 On Force |
| 1076 | 0 | 0-255 | Key 107 Force Curve ID |
| 1077 | 376 | 0-376 | Key 107 Max Force |
| 1078 | 3 | 1-255 | Key 107 Retro Divisor |
| 1079 | 100 | 0-65535 | Key 107 Retro Time(ms) |
| 1080 | 0 | 0-30000 | Key 107 Max On Time(ms) |
| 1100 | 72 | 0-376 | Key 12 On Force |
| 1101 | 0 | 0-255 | Key 12 Force Curve ID |
| 1102 | 376 | 0-376 | Key 12 Max Force |
| 1103 | 3 | 1-255 | Key 12 Retro Divisor |
| 1104 | 100 | 0-65535 | Key 12 Retro Time(ms) |
| 1105 | 0 | 0-30000 | Key 12 Max On Time(ms) |
| 1125 | 65 | 0-376 | Key 108 On Force |
| 1126 | 0 | 0-255 | Key 108 Force Curve ID |
| 1127 | 376 | 0-376 | Key 108 Max Force |
| 1128 | 3 | 1-255 | Key 108 Retro Divisor |
| 1129 | 100 | 0-65535 | Key 108 Retro Time(ms) |
| 1130 | 0 | 0-30000 | Key 108 Max On Time(ms) |
| 1150 | 68 | 0-376 | Key 13 On Force |
| 1151 | 0 | 0-255 | Key 13 Force Curve ID |
| 1152 | 376 | 0-376 | Key 13 Max Force |
| 1153 | 3 | 1-255 | Key 13 Retro Divisor |
| 1154 | 100 | 0-65535 | Key 13 Retro Time(ms) |
| 1155 | 0 | 0-30000 | Key 13 Max On Time(ms) |
| 1175 | 65 | 0-376 | Key 109 On Force |
| 1176 | 0 | 0-255 | Key 109 Force Curve ID |
| 1177 | 376 | 0-376 | Key 109 Max Force |
| 1178 | 3 | 1-255 | Key 109 Retro Divisor |
| 1179 | 100 | 0-65535 | Key 109 Retro Time(ms) |
| 1180 | 0 | 0-30000 | Key 109 Max On Time(ms) |
| 1200 | 70 | 0-376 | Key 14 On Force |
| 1201 | 0 | 0-255 | Key 14 Force Curve ID |
| 1202 | 376 | 0-376 | Key 14 Max Force |
| 1203 | 3 | 1-255 | Key 14 Retro Divisor |
| 1204 | 100 | 0-65535 | Key 14 Retro Time(ms) |
| 1205 | 0 | 0-30000 | Key 14 Max On Time(ms) |
| 1225 | 65 | 0-376 | Key 110 On Force |
| 1226 | 0 | 0-255 | Key 110 Force Curve ID |
| 1227 | 376 | 0-376 | Key 110 Max Force |
| 1228 | 3 | 1-255 | Key 110 Retro Divisor |
| 1229 | 100 | 0-65535 | Key 110 Retro Time(ms) |
| 1230 | 0 | 0-30000 | Key 110 Max On Time(ms) |
| 1250 | 65 | 0-376 | Key 15 On Force |
| 1251 | 0 | 0-255 | Key 15 Force Curve ID |
| 1252 | 376 | 0-376 | Key 15 Max Force |
| 1253 | 3 | 1-255 | Key 15 Retro Divisor |
| 1254 | 100 | 0-65535 | Key 15 Retro Time(ms) |
| 1255 | 0 | 0-30000 | Key 15 Max On Time(ms) |
| 1275 | 65 | 0-376 | Key 111 On Force |
| 1276 | 0 | 0-255 | Key 111 Force Curve ID |
| 1277 | 376 | 0-376 | Key 111 Max Force |
| 1278 | 3 | 1-255 | Key 111 Retro Divisor |
| 1279 | 100 | 0-65535 | Key 111 Retro Time(ms) |
| 1280 | 0 | 0-30000 | Key 111 Max On Time(ms) |
| 1300 | 70 | 0-376 | Key 16 On Force |
| 1301 | 0 | 0-255 | Key 16 Force Curve ID |
| 1302 | 376 | 0-376 | Key 16 Max Force |
| 1303 | 3 | 1-255 | Key 16 Retro Divisor |
| 1304 | 100 | 0-65535 | Key 16 Retro Time(ms) |
| 1305 | 0 | 0-30000 | Key 16 Max On Time(ms) |
| 1325 | 65 | 0-376 | Key 112 On Force |
| 1326 | 0 | 0-255 | Key 112 Force Curve ID |
| 1327 | 376 | 0-376 | Key 112 Max Force |
| 1328 | 3 | 1-255 | Key 112 Retro Divisor |
| 1329 | 100 | 0-65535 | Key 112 Retro Time(ms) |
| 1330 | 0 | 0-30000 | Key 112 Max On Time(ms) |
| 1350 | 61 | 0-376 | Key 17 On Force |
| 1351 | 0 | 0-255 | Key 17 Force Curve ID |
| 1352 | 376 | 0-376 | Key 17 Max Force |
| 1353 | 3 | 1-255 | Key 17 Retro Divisor |
| 1354 | 100 | 0-65535 | Key 17 Retro Time(ms) |
| 1355 | 0 | 0-30000 | Key 17 Max On Time(ms) |
| 1375 | 65 | 0-376 | Key 113 On Force |
| 1376 | 0 | 0-255 | Key 113 Force Curve ID |
| 1377 | 376 | 0-376 | Key 113 Max Force |
| 1378 | 3 | 1-255 | Key 113 Retro Divisor |
| 1379 | 100 | 0-65535 | Key 113 Retro Time(ms) |
| 1380 | 0 | 0-30000 | Key 113 Max On Time(ms) |
| 1400 | 68 | 0-376 | Key 18 On Force |
| 1401 | 0 | 0-255 | Key 18 Force Curve ID |
| 1402 | 376 | 0-376 | Key 18 Max Force |
| 1403 | 3 | 1-255 | Key 18 Retro Divisor |
| 1404 | 100 | 0-65535 | Key 18 Retro Time(ms) |
| 1405 | 0 | 0-30000 | Key 18 Max On Time(ms) |
| 1425 | 65 | 0-376 | Key 114 On Force |
| 1426 | 0 | 0-255 | Key 114 Force Curve ID |
| 1427 | 376 | 0-376 | Key 114 Max Force |
| 1428 | 3 | 1-255 | Key 114 Retro Divisor |
| 1429 | 100 | 0-65535 | Key 114 Retro Time(ms) |
| 1430 | 0 | 0-30000 | Key 114 Max On Time(ms) |
| 1450 | 66 | 0-376 | Key 19 On Force |
| 1451 | 0 | 0-255 | Key 19 Force Curve ID |
| 1452 | 376 | 0-376 | Key 19 Max Force |
| 1453 | 3 | 1-255 | Key 19 Retro Divisor |
| 1454 | 100 | 0-65535 | Key 19 Retro Time(ms) |
| 1455 | 0 | 0-30000 | Key 19 Max On Time(ms) |
| 1475 | 65 | 0-376 | Key 115 On Force |
| 1476 | 0 | 0-255 | Key 115 Force Curve ID |
| 1477 | 376 | 0-376 | Key 115 Max Force |
| 1478 | 3 | 1-255 | Key 115 Retro Divisor |
| 1479 | 100 | 0-65535 | Key 115 Retro Time(ms) |
| 1480 | 0 | 0-30000 | Key 115 Max On Time(ms) |
| 1500 | 54 | 0-376 | Key 20 On Force |
| 1501 | 0 | 0-255 | Key 20 Force Curve ID |
| 1502 | 376 | 0-376 | Key 20 Max Force |
| 1503 | 3 | 1-255 | Key 20 Retro Divisor |
| 1504 | 100 | 0-65535 | Key 20 Retro Time(ms) |
| 1505 | 0 | 0-30000 | Key 20 Max On Time(ms) |
| 1525 | 65 | 0-376 | Key 116 On Force |
| 1526 | 0 | 0-255 | Key 116 Force Curve ID |
| 1527 | 376 | 0-376 | Key 116 Max Force |
| 1528 | 3 | 1-255 | Key 116 Retro Divisor |
| 1529 | 100 | 0-65535 | Key 116 Retro Time(ms) |
| 1530 | 0 | 0-30000 | Key 116 Max On Time(ms) |
| 1550 | 67 | 0-376 | Key 21 On Force |
| 1551 | 0 | 0-255 | Key 21 Force Curve ID |
| 1552 | 376 | 0-376 | Key 21 Max Force |
| 1553 | 3 | 1-255 | Key 21 Retro Divisor |
| 1554 | 100 | 0-65535 | Key 21 Retro Time(ms) |
| 1555 | 0 | 0-30000 | Key 21 Max On Time(ms) |
| 1575 | 65 | 0-376 | Key 117 On Force |
| 1576 | 0 | 0-255 | Key 117 Force Curve ID |
| 1577 | 376 | 0-376 | Key 117 Max Force |
| 1578 | 3 | 1-255 | Key 117 Retro Divisor |
| 1579 | 100 | 0-65535 | Key 117 Retro Time(ms) |
| 1580 | 0 | 0-30000 | Key 117 Max On Time(ms) |
| 1600 | 72 | 0-376 | Key 22 On Force |
| 1601 | 0 | 0-255 | Key 22 Force Curve ID |
| 1602 | 376 | 0-376 | Key 22 Max Force |
| 1603 | 3 | 1-255 | Key 22 Retro Divisor |
| 1604 | 100 | 0-65535 | Key 22 Retro Time(ms) |
| 1605 | 0 | 0-30000 | Key 22 Max On Time(ms) |
| 1625 | 65 | 0-376 | Key 118 On Force |
| 1626 | 0 | 0-255 | Key 118 Force Curve ID |
| 1627 | 376 | 0-376 | Key 118 Max Force |
| 1628 | 3 | 1-255 | Key 118 Retro Divisor |
| 1629 | 100 | 0-65535 | Key 118 Retro Time(ms) |
| 1630 | 0 | 0-30000 | Key 118 Max On Time(ms) |
| 1650 | 57 | 0-376 | Key 23 On Force |
| 1651 | 0 | 0-255 | Key 23 Force Curve ID |
| 1652 | 376 | 0-376 | Key 23 Max Force |
| 1653 | 3 | 1-255 | Key 23 Retro Divisor |
| 1654 | 100 | 0-65535 | Key 23 Retro Time(ms) |
| 1655 | 0 | 0-30000 | Key 23 Max On Time(ms) |
| 1675 | 65 | 0-376 | Key 119 On Force |
| 1676 | 0 | 0-255 | Key 119 Force Curve ID |
| 1677 | 376 | 0-376 | Key 119 Max Force |
| 1678 | 3 | 1-255 | Key 119 Retro Divisor |
| 1679 | 100 | 0-65535 | Key 119 Retro Time(ms) |
| 1680 | 0 | 0-30000 | Key 119 Max On Time(ms) |
| 1700 | 64 | 0-376 | Key 24 On Force |
| 1701 | 0 | 0-255 | Key 24 Force Curve ID |
| 1702 | 376 | 0-376 | Key 24 Max Force |
| 1703 | 3 | 1-255 | Key 24 Retro Divisor |
| 1704 | 100 | 0-65535 | Key 24 Retro Time(ms) |
| 1705 | 0 | 0-30000 | Key 24 Max On Time(ms) |
| 1725 | 65 | 0-376 | Key 120 On Force |
| 1726 | 0 | 0-255 | Key 120 Force Curve ID |
| 1727 | 376 | 0-376 | Key 120 Max Force |
| 1728 | 3 | 1-255 | Key 120 Retro Divisor |
| 1729 | 100 | 0-65535 | Key 120 Retro Time(ms) |
| 1730 | 0 | 0-30000 | Key 120 Max On Time(ms) |
| 1750 | 62 | 0-376 | Key 25 On Force |
| 1751 | 0 | 0-255 | Key 25 Force Curve ID |
| 1752 | 376 | 0-376 | Key 25 Max Force |
| 1753 | 3 | 1-255 | Key 25 Retro Divisor |
| 1754 | 100 | 0-65535 | Key 25 Retro Time(ms) |
| 1755 | 0 | 0-30000 | Key 25 Max On Time(ms) |
| 1775 | 65 | 0-376 | Key 121 On Force |
| 1776 | 0 | 0-255 | Key 121 Force Curve ID |
| 1777 | 376 | 0-376 | Key 121 Max Force |
| 1778 | 3 | 1-255 | Key 121 Retro Divisor |
| 1779 | 100 | 0-65535 | Key 121 Retro Time(ms) |
| 1780 | 0 | 0-30000 | Key 121 Max On Time(ms) |
| 1800 | 70 | 0-376 | Key 26 On Force |
| 1801 | 0 | 0-255 | Key 26 Force Curve ID |
| 1802 | 376 | 0-376 | Key 26 Max Force |
| 1803 | 3 | 1-255 | Key 26 Retro Divisor |
| 1804 | 100 | 0-65535 | Key 26 Retro Time(ms) |
| 1805 | 0 | 0-30000 | Key 26 Max On Time(ms) |
| 1825 | 65 | 0-376 | Key 122 On Force |
| 1826 | 0 | 0-255 | Key 122 Force Curve ID |
| 1827 | 376 | 0-376 | Key 122 Max Force |
| 1828 | 3 | 1-255 | Key 122 Retro Divisor |
| 1829 | 100 | 0-65535 | Key 122 Retro Time(ms) |
| 1830 | 0 | 0-30000 | Key 122 Max On Time(ms) |
| 1850 | 58 | 0-376 | Key 27 On Force |
| 1851 | 0 | 0-255 | Key 27 Force Curve ID |
| 1852 | 376 | 0-376 | Key 27 Max Force |
| 1853 | 3 | 1-255 | Key 27 Retro Divisor |
| 1854 | 100 | 0-65535 | Key 27 Retro Time(ms) |
| 1855 | 0 | 0-30000 | Key 27 Max On Time(ms) |
| 1875 | 65 | 0-376 | Key 123 On Force |
| 1876 | 0 | 0-255 | Key 123 Force Curve ID |
| 1877 | 376 | 0-376 | Key 123 Max Force |
| 1878 | 3 | 1-255 | Key 123 Retro Divisor |
| 1879 | 100 | 0-65535 | Key 123 Retro Time(ms) |
| 1880 | 0 | 0-30000 | Key 123 Max On Time(ms) |
| 1900 | 54 | 0-376 | Key 28 On Force |
| 1901 | 0 | 0-255 | Key 28 Force Curve ID |
| 1902 | 376 | 0-376 | Key 28 Max Force |
| 1903 | 3 | 1-255 | Key 28 Retro Divisor |
| 1904 | 100 | 0-65535 | Key 28 Retro Time(ms) |
| 1905 | 0 | 0-30000 | Key 28 Max On Time(ms) |
| 1925 | 65 | 0-376 | Key 124 On Force |
| 1926 | 0 | 0-255 | Key 124 Force Curve ID |
| 1927 | 376 | 0-376 | Key 124 Max Force |
| 1928 | 3 | 1-255 | Key 124 Retro Divisor |
| 1929 | 100 | 0-65535 | Key 124 Retro Time(ms) |
| 1930 | 0 | 0-30000 | Key 124 Max On Time(ms) |
| 1950 | 56 | 0-376 | Key 29 On Force |
| 1951 | 0 | 0-255 | Key 29 Force Curve ID |
| 1952 | 376 | 0-376 | Key 29 Max Force |
| 1953 | 3 | 1-255 | Key 29 Retro Divisor |
| 1954 | 100 | 0-65535 | Key 29 Retro Time(ms) |
| 1955 | 0 | 0-30000 | Key 29 Max On Time(ms) |
| 1975 | 65 | 0-376 | Key 125 On Force |
| 1976 | 0 | 0-255 | Key 125 Force Curve ID |
| 1977 | 376 | 0-376 | Key 125 Max Force |
| 1978 | 3 | 1-255 | Key 125 Retro Divisor |
| 1979 | 100 | 0-65535 | Key 125 Retro Time(ms) |
| 1980 | 0 | 0-30000 | Key 125 Max On Time(ms) |
| 2000 | 53 | 0-376 | Key 30 On Force |
| 2001 | 0 | 0-255 | Key 30 Force Curve ID |
| 2002 | 376 | 0-376 | Key 30 Max Force |
| 2003 | 3 | 1-255 | Key 30 Retro Divisor |
| 2004 | 100 | 0-65535 | Key 30 Retro Time(ms) |
| 2005 | 0 | 0-30000 | Key 30 Max On Time(ms) |
| 2025 | 65 | 0-376 | Key 126 On Force |
| 2026 | 0 | 0-255 | Key 126 Force Curve ID |
| 2027 | 376 | 0-376 | Key 126 Max Force |
| 2028 | 3 | 1-255 | Key 126 Retro Divisor |
| 2029 | 100 | 0-65535 | Key 126 Retro Time(ms) |
| 2030 | 0 | 0-30000 | Key 126 Max On Time(ms) |
| 2050 | 57 | 0-376 | Key 31 On Force |
| 2051 | 0 | 0-255 | Key 31 Force Curve ID |
| 2052 | 376 | 0-376 | Key 31 Max Force |
| 2053 | 3 | 1-255 | Key 31 Retro Divisor |
| 2054 | 100 | 0-65535 | Key 31 Retro Time(ms) |
| 2055 | 0 | 0-30000 | Key 31 Max On Time(ms) |
| 2075 | 65 | 0-376 | Key 127 On Force |
| 2076 | 0 | 0-255 | Key 127 Force Curve ID |
| 2077 | 376 | 0-376 | Key 127 Max Force |
| 2078 | 3 | 1-255 | Key 127 Retro Divisor |
| 2079 | 100 | 0-65535 | Key 127 Retro Time(ms) |
| 2080 | 0 | 0-30000 | Key 127 Max On Time(ms) |
| 2100 | 62 | 0-376 | Key 32 On Force |
| 2101 | 0 | 0-255 | Key 32 Force Curve ID |
| 2102 | 376 | 0-376 | Key 32 Max Force |
| 2103 | 3 | 1-255 | Key 32 Retro Divisor |
| 2104 | 100 | 0-65535 | Key 32 Retro Time(ms) |
| 2105 | 0 | 0-30000 | Key 32 Max On Time(ms) |
| 2150 | 58 | 0-376 | Key 33 On Force |
| 2151 | 0 | 0-255 | Key 33 Force Curve ID |
| 2152 | 376 | 0-376 | Key 33 Max Force |
| 2153 | 3 | 1-255 | Key 33 Retro Divisor |
| 2154 | 100 | 0-65535 | Key 33 Retro Time(ms) |
| 2155 | 0 | 0-30000 | Key 33 Max On Time(ms) |
| 2200 | 58 | 0-376 | Key 34 On Force |
| 2201 | 0 | 0-255 | Key 34 Force Curve ID |
| 2202 | 376 | 0-376 | Key 34 Max Force |
| 2203 | 3 | 1-255 | Key 34 Retro Divisor |
| 2204 | 100 | 0-65535 | Key 34 Retro Time(ms) |
| 2205 | 0 | 0-30000 | Key 34 Max On Time(ms) |
| 2250 | 58 | 0-376 | Key 35 On Force |
| 2251 | 0 | 0-255 | Key 35 Force Curve ID |
| 2252 | 376 | 0-376 | Key 35 Max Force |
| 2253 | 3 | 1-255 | Key 35 Retro Divisor |
| 2254 | 100 | 0-65535 | Key 35 Retro Time(ms) |
| 2255 | 0 | 0-30000 | Key 35 Max On Time(ms) |
| 2300 | 50 | 0-376 | Key 36 On Force |
| 2301 | 0 | 0-255 | Key 36 Force Curve ID |
| 2302 | 376 | 0-376 | Key 36 Max Force |
| 2303 | 3 | 1-255 | Key 36 Retro Divisor |
| 2304 | 100 | 0-65535 | Key 36 Retro Time(ms) |
| 2305 | 0 | 0-30000 | Key 36 Max On Time(ms) |
| 2350 | 56 | 0-376 | Key 37 On Force |
| 2351 | 0 | 0-255 | Key 37 Force Curve ID |
| 2352 | 376 | 0-376 | Key 37 Max Force |
| 2353 | 3 | 1-255 | Key 37 Retro Divisor |
| 2354 | 100 | 0-65535 | Key 37 Retro Time(ms) |
| 2355 | 0 | 0-30000 | Key 37 Max On Time(ms) |
| 2400 | 57 | 0-376 | Key 38 On Force |
| 2401 | 0 | 0-255 | Key 38 Force Curve ID |
| 2402 | 376 | 0-376 | Key 38 Max Force |
| 2403 | 3 | 1-255 | Key 38 Retro Divisor |
| 2404 | 100 | 0-65535 | Key 38 Retro Time(ms) |
| 2405 | 0 | 0-30000 | Key 38 Max On Time(ms) |
| 2450 | 61 | 0-376 | Key 39 On Force |
| 2451 | 0 | 0-255 | Key 39 Force Curve ID |
| 2452 | 376 | 0-376 | Key 39 Max Force |
| 2453 | 3 | 1-255 | Key 39 Retro Divisor |
| 2454 | 100 | 0-65535 | Key 39 Retro Time(ms) |
| 2455 | 0 | 0-30000 | Key 39 Max On Time(ms) |
| 2500 | 52 | 0-376 | Key 40 On Force |
| 2501 | 0 | 0-255 | Key 40 Force Curve ID |
| 2502 | 376 | 0-376 | Key 40 Max Force |
| 2503 | 3 | 1-255 | Key 40 Retro Divisor |
| 2504 | 100 | 0-65535 | Key 40 Retro Time(ms) |
| 2505 | 0 | 0-30000 | Key 40 Max On Time(ms) |
| 2550 | 59 | 0-376 | Key 41 On Force |
| 2551 | 0 | 0-255 | Key 41 Force Curve ID |
| 2552 | 376 | 0-376 | Key 41 Max Force |
| 2553 | 3 | 1-255 | Key 41 Retro Divisor |
| 2554 | 100 | 0-65535 | Key 41 Retro Time(ms) |
| 2555 | 0 | 0-30000 | Key 41 Max On Time(ms) |
| 2600 | 57 | 0-376 | Key 42 On Force |
| 2601 | 0 | 0-255 | Key 42 Force Curve ID |
| 2602 | 376 | 0-376 | Key 42 Max Force |
| 2603 | 3 | 1-255 | Key 42 Retro Divisor |
| 2604 | 100 | 0-65535 | Key 42 Retro Time(ms) |
| 2605 | 0 | 0-30000 | Key 42 Max On Time(ms) |
| 2650 | 53 | 0-376 | Key 43 On Force |
| 2651 | 0 | 0-255 | Key 43 Force Curve ID |
| 2652 | 376 | 0-376 | Key 43 Max Force |
| 2653 | 3 | 1-255 | Key 43 Retro Divisor |
| 2654 | 100 | 0-65535 | Key 43 Retro Time(ms) |
| 2655 | 0 | 0-30000 | Key 43 Max On Time(ms) |
| 2700 | 54 | 0-376 | Key 44 On Force |
| 2701 | 0 | 0-255 | Key 44 Force Curve ID |
| 2702 | 376 | 0-376 | Key 44 Max Force |
| 2703 | 3 | 1-255 | Key 44 Retro Divisor |
| 2704 | 100 | 0-65535 | Key 44 Retro Time(ms) |
| 2705 | 0 | 0-30000 | Key 44 Max On Time(ms) |
| 2750 | 56 | 0-376 | Key 45 On Force |
| 2751 | 0 | 0-255 | Key 45 Force Curve ID |
| 2752 | 376 | 0-376 | Key 45 Max Force |
| 2753 | 3 | 1-255 | Key 45 Retro Divisor |
| 2754 | 100 | 0-65535 | Key 45 Retro Time(ms) |
| 2755 | 0 | 0-30000 | Key 45 Max On Time(ms) |
| 2800 | 64 | 0-376 | Key 46 On Force |
| 2801 | 0 | 0-255 | Key 46 Force Curve ID |
| 2802 | 376 | 0-376 | Key 46 Max Force |
| 2803 | 3 | 1-255 | Key 46 Retro Divisor |
| 2804 | 100 | 0-65535 | Key 46 Retro Time(ms) |
| 2805 | 0 | 0-30000 | Key 46 Max On Time(ms) |
| 2850 | 52 | 0-376 | Key 47 On Force |
| 2851 | 0 | 0-255 | Key 47 Force Curve ID |
| 2852 | 376 | 0-376 | Key 47 Max Force |
| 2853 | 3 | 1-255 | Key 47 Retro Divisor |
| 2854 | 100 | 0-65535 | Key 47 Retro Time(ms) |
| 2855 | 0 | 0-30000 | Key 47 Max On Time(ms) |
| 2900 | 56 | 0-376 | Key 48 On Force |
| 2901 | 0 | 0-255 | Key 48 Force Curve ID |
| 2902 | 376 | 0-376 | Key 48 Max Force |
| 2903 | 3 | 1-255 | Key 48 Retro Divisor |
| 2904 | 100 | 0-65535 | Key 48 Retro Time(ms) |
| 2905 | 0 | 0-30000 | Key 48 Max On Time(ms) |
| 2950 | 62 | 0-376 | Key 49 On Force |
| 2951 | 0 | 0-255 | Key 49 Force Curve ID |
| 2952 | 376 | 0-376 | Key 49 Max Force |
| 2953 | 3 | 1-255 | Key 49 Retro Divisor |
| 2954 | 100 | 0-65535 | Key 49 Retro Time(ms) |
| 2955 | 0 | 0-30000 | Key 49 Max On Time(ms) |
| 3000 | 54 | 0-376 | Key 50 On Force |
| 3001 | 0 | 0-255 | Key 50 Force Curve ID |
| 3002 | 376 | 0-376 | Key 50 Max Force |
| 3003 | 3 | 1-255 | Key 50 Retro Divisor |
| 3004 | 100 | 0-65535 | Key 50 Retro Time(ms) |
| 3005 | 0 | 0-30000 | Key 50 Max On Time(ms) |
| 3050 | 60 | 0-376 | Key 51 On Force |
| 3051 | 0 | 0-255 | Key 51 Force Curve ID |
| 3052 | 376 | 0-376 | Key 51 Max Force |
| 3053 | 3 | 1-255 | Key 51 Retro Divisor |
| 3054 | 100 | 0-65535 | Key 51 Retro Time(ms) |
| 3055 | 0 | 0-30000 | Key 51 Max On Time(ms) |
| 3100 | 52 | 0-376 | Key 52 On Force |
| 3101 | 0 | 0-255 | Key 52 Force Curve ID |
| 3102 | 376 | 0-376 | Key 52 Max Force |
| 3103 | 3 | 1-255 | Key 52 Retro Divisor |
| 3104 | 100 | 0-65535 | Key 52 Retro Time(ms) |
| 3105 | 0 | 0-30000 | Key 52 Max On Time(ms) |
| 3150 | 48 | 0-376 | Key 53 On Force |
| 3151 | 0 | 0-255 | Key 53 Force Curve ID |
| 3152 | 376 | 0-376 | Key 53 Max Force |
| 3153 | 3 | 1-255 | Key 53 Retro Divisor |
| 3154 | 100 | 0-65535 | Key 53 Retro Time(ms) |
| 3155 | 0 | 0-30000 | Key 53 Max On Time(ms) |
| 3200 | 56 | 0-376 | Key 54 On Force |
| 3201 | 0 | 0-255 | Key 54 Force Curve ID |
| 3202 | 376 | 0-376 | Key 54 Max Force |
| 3203 | 3 | 1-255 | Key 54 Retro Divisor |
| 3204 | 100 | 0-65535 | Key 54 Retro Time(ms) |
| 3205 | 0 | 0-30000 | Key 54 Max On Time(ms) |
| 3250 | 51 | 0-376 | Key 55 On Force |
| 3251 | 0 | 0-255 | Key 55 Force Curve ID |
| 3252 | 376 | 0-376 | Key 55 Max Force |
| 3253 | 3 | 1-255 | Key 55 Retro Divisor |
| 3254 | 100 | 0-65535 | Key 55 Retro Time(ms) |
| 3255 | 0 | 0-30000 | Key 55 Max On Time(ms) |
| 3300 | 54 | 0-376 | Key 56 On Force |
| 3301 | 0 | 0-255 | Key 56 Force Curve ID |
| 3302 | 376 | 0-376 | Key 56 Max Force |
| 3303 | 3 | 1-255 | Key 56 Retro Divisor |
| 3304 | 100 | 0-65535 | Key 56 Retro Time(ms) |
| 3305 | 0 | 0-30000 | Key 56 Max On Time(ms) |
| 3350 | 49 | 0-376 | Key 57 On Force |
| 3351 | 0 | 0-255 | Key 57 Force Curve ID |
| 3352 | 376 | 0-376 | Key 57 Max Force |
| 3353 | 3 | 1-255 | Key 57 Retro Divisor |
| 3354 | 100 | 0-65535 | Key 57 Retro Time(ms) |
| 3355 | 0 | 0-30000 | Key 57 Max On Time(ms) |
| 3400 | 56 | 0-376 | Key 58 On Force |
| 3401 | 0 | 0-255 | Key 58 Force Curve ID |
| 3402 | 376 | 0-376 | Key 58 Max Force |
| 3403 | 3 | 1-255 | Key 58 Retro Divisor |
| 3404 | 100 | 0-65535 | Key 58 Retro Time(ms) |
| 3405 | 0 | 0-30000 | Key 58 Max On Time(ms) |
| 3450 | 52 | 0-376 | Key 59 On Force |
| 3451 | 0 | 0-255 | Key 59 Force Curve ID |
| 3452 | 376 | 0-376 | Key 59 Max Force |
| 3453 | 3 | 1-255 | Key 59 Retro Divisor |
| 3454 | 100 | 0-65535 | Key 59 Retro Time(ms) |
| 3455 | 0 | 0-30000 | Key 59 Max On Time(ms) |
| 3500 | 47 | 0-376 | Key 60 On Force |
| 3501 | 0 | 0-255 | Key 60 Force Curve ID |
| 3502 | 376 | 0-376 | Key 60 Max Force |
| 3503 | 3 | 1-255 | Key 60 Retro Divisor |
| 3504 | 100 | 0-65535 | Key 60 Retro Time(ms) |
| 3505 | 0 | 0-30000 | Key 60 Max On Time(ms) |
| 3550 | 50 | 0-376 | Key 61 On Force |
| 3551 | 0 | 0-255 | Key 61 Force Curve ID |
| 3552 | 376 | 0-376 | Key 61 Max Force |
| 3553 | 3 | 1-255 | Key 61 Retro Divisor |
| 3554 | 100 | 0-65535 | Key 61 Retro Time(ms) |
| 3555 | 0 | 0-30000 | Key 61 Max On Time(ms) |
| 3600 | 56 | 0-376 | Key 62 On Force |
| 3601 | 0 | 0-255 | Key 62 Force Curve ID |
| 3602 | 376 | 0-376 | Key 62 Max Force |
| 3603 | 3 | 1-255 | Key 62 Retro Divisor |
| 3604 | 100 | 0-65535 | Key 62 Retro Time(ms) |
| 3605 | 0 | 0-30000 | Key 62 Max On Time(ms) |
| 3650 | 52 | 0-376 | Key 63 On Force |
| 3651 | 0 | 0-255 | Key 63 Force Curve ID |
| 3652 | 376 | 0-376 | Key 63 Max Force |
| 3653 | 3 | 1-255 | Key 63 Retro Divisor |
| 3654 | 100 | 0-65535 | Key 63 Retro Time(ms) |
| 3655 | 0 | 0-30000 | Key 63 Max On Time(ms) |
| 3700 | 58 | 0-376 | Key 64 On Force |
| 3701 | 0 | 0-255 | Key 64 Force Curve ID |
| 3702 | 376 | 0-376 | Key 64 Max Force |
| 3703 | 3 | 1-255 | Key 64 Retro Divisor |
| 3704 | 100 | 0-65535 | Key 64 Retro Time(ms) |
| 3705 | 0 | 0-30000 | Key 64 Max On Time(ms) |
| 3750 | 48 | 0-376 | Key 65 On Force |
| 3751 | 0 | 0-255 | Key 65 Force Curve ID |
| 3752 | 376 | 0-376 | Key 65 Max Force |
| 3753 | 3 | 1-255 | Key 65 Retro Divisor |
| 3754 | 100 | 0-65535 | Key 65 Retro Time(ms) |
| 3755 | 0 | 0-30000 | Key 65 Max On Time(ms) |
| 3800 | 48 | 0-376 | Key 66 On Force |
| 3801 | 0 | 0-255 | Key 66 Force Curve ID |
| 3802 | 376 | 0-376 | Key 66 Max Force |
| 3803 | 3 | 1-255 | Key 66 Retro Divisor |
| 3804 | 100 | 0-65535 | Key 66 Retro Time(ms) |
| 3805 | 0 | 0-30000 | Key 66 Max On Time(ms) |
| 3850 | 43 | 0-376 | Key 67 On Force |
| 3851 | 0 | 0-255 | Key 67 Force Curve ID |
| 3852 | 376 | 0-376 | Key 67 Max Force |
| 3853 | 3 | 1-255 | Key 67 Retro Divisor |
| 3854 | 100 | 0-65535 | Key 67 Retro Time(ms) |
| 3855 | 0 | 0-30000 | Key 67 Max On Time(ms) |
| 3900 | 48 | 0-376 | Key 68 On Force |
| 3901 | 0 | 0-255 | Key 68 Force Curve ID |
| 3902 | 376 | 0-376 | Key 68 Max Force |
| 3903 | 3 | 1-255 | Key 68 Retro Divisor |
| 3904 | 100 | 0-65535 | Key 68 Retro Time(ms) |
| 3905 | 0 | 0-30000 | Key 68 Max On Time(ms) |
| 3950 | 44 | 0-376 | Key 69 On Force |
| 3951 | 0 | 0-255 | Key 69 Force Curve ID |
| 3952 | 376 | 0-376 | Key 69 Max Force |
| 3953 | 3 | 1-255 | Key 69 Retro Divisor |
| 3954 | 100 | 0-65535 | Key 69 Retro Time(ms) |
| 3955 | 0 | 0-30000 | Key 69 Max On Time(ms) |
| 4000 | 47 | 0-376 | Key 70 On Force |
| 4001 | 0 | 0-255 | Key 70 Force Curve ID |
| 4002 | 376 | 0-376 | Key 70 Max Force |
| 4003 | 3 | 1-255 | Key 70 Retro Divisor |
| 4004 | 100 | 0-65535 | Key 70 Retro Time(ms) |
| 4005 | 0 | 0-30000 | Key 70 Max On Time(ms) |
| 4050 | 44 | 0-376 | Key 71 On Force |
| 4051 | 0 | 0-255 | Key 71 Force Curve ID |
| 4052 | 376 | 0-376 | Key 71 Max Force |
| 4053 | 3 | 1-255 | Key 71 Retro Divisor |
| 4054 | 100 | 0-65535 | Key 71 Retro Time(ms) |
| 4055 | 0 | 0-30000 | Key 71 Max On Time(ms) |
| 4100 | 49 | 0-376 | Key 72 On Force |
| 4101 | 0 | 0-255 | Key 72 Force Curve ID |
| 4102 | 376 | 0-376 | Key 72 Max Force |
| 4103 | 3 | 1-255 | Key 72 Retro Divisor |
| 4104 | 100 | 0-65535 | Key 72 Retro Time(ms) |
| 4105 | 0 | 0-30000 | Key 72 Max On Time(ms) |
| 4150 | 46 | 0-376 | Key 73 On Force |
| 4151 | 0 | 0-255 | Key 73 Force Curve ID |
| 4152 | 376 | 0-376 | Key 73 Max Force |
| 4153 | 3 | 1-255 | Key 73 Retro Divisor |
| 4154 | 100 | 0-65535 | Key 73 Retro Time(ms) |
| 4155 | 0 | 0-30000 | Key 73 Max On Time(ms) |
| 4200 | 44 | 0-376 | Key 74 On Force |
| 4201 | 0 | 0-255 | Key 74 Force Curve ID |
| 4202 | 376 | 0-376 | Key 74 Max Force |
| 4203 | 3 | 1-255 | Key 74 Retro Divisor |
| 4204 | 100 | 0-65535 | Key 74 Retro Time(ms) |
| 4205 | 0 | 0-30000 | Key 74 Max On Time(ms) |
| 4250 | 48 | 0-376 | Key 75 On Force |
| 4251 | 0 | 0-255 | Key 75 Force Curve ID |
| 4252 | 376 | 0-376 | Key 75 Max Force |
| 4253 | 3 | 1-255 | Key 75 Retro Divisor |
| 4254 | 100 | 0-65535 | Key 75 Retro Time(ms) |
| 4255 | 0 | 0-30000 | Key 75 Max On Time(ms) |
| 4300 | 48 | 0-376 | Key 76 On Force |
| 4301 | 0 | 0-255 | Key 76 Force Curve ID |
| 4302 | 376 | 0-376 | Key 76 Max Force |
| 4303 | 3 | 1-255 | Key 76 Retro Divisor |
| 4304 | 100 | 0-65535 | Key 76 Retro Time(ms) |
| 4305 | 0 | 0-30000 | Key 76 Max On Time(ms) |
| 4350 | 44 | 0-376 | Key 77 On Force |
| 4351 | 0 | 0-255 | Key 77 Force Curve ID |
| 4352 | 376 | 0-376 | Key 77 Max Force |
| 4353 | 3 | 1-255 | Key 77 Retro Divisor |
| 4354 | 100 | 0-65535 | Key 77 Retro Time(ms) |
| 4355 | 0 | 0-30000 | Key 77 Max On Time(ms) |
| 4400 | 65 | 0-376 | Key 78 On Force |
| 4401 | 0 | 0-255 | Key 78 Force Curve ID |
| 4402 | 376 | 0-376 | Key 78 Max Force |
| 4403 | 3 | 1-255 | Key 78 Retro Divisor |
| 4404 | 100 | 0-65535 | Key 78 Retro Time(ms) |
| 4405 | 0 | 0-30000 | Key 78 Max On Time(ms) |
| 4450 | 65 | 0-376 | Key 79 On Force |
| 4451 | 0 | 0-255 | Key 79 Force Curve ID |
| 4452 | 376 | 0-376 | Key 79 Max Force |
| 4453 | 3 | 1-255 | Key 79 Retro Divisor |
| 4454 | 100 | 0-65535 | Key 79 Retro Time(ms) |
| 4455 | 0 | 0-30000 | Key 79 Max On Time(ms) |
| 4500 | 65 | 0-376 | Key 80 On Force |
| 4501 | 0 | 0-255 | Key 80 Force Curve ID |
| 4502 | 376 | 0-376 | Key 80 Max Force |
| 4503 | 3 | 1-255 | Key 80 Retro Divisor |
| 4504 | 100 | 0-65535 | Key 80 Retro Time(ms) |
| 4505 | 0 | 0-30000 | Key 80 Max On Time(ms) |
| 4550 | 65 | 0-376 | Key 81 On Force |
| 4551 | 0 | 0-255 | Key 81 Force Curve ID |
| 4552 | 376 | 0-376 | Key 81 Max Force |
| 4553 | 3 | 1-255 | Key 81 Retro Divisor |
| 4554 | 100 | 0-65535 | Key 81 Retro Time(ms) |
| 4555 | 0 | 0-30000 | Key 81 Max On Time(ms) |
| 4600 | 65 | 0-376 | Key 82 On Force |
| 4601 | 0 | 0-255 | Key 82 Force Curve ID |
| 4602 | 376 | 0-376 | Key 82 Max Force |
| 4603 | 3 | 1-255 | Key 82 Retro Divisor |
| 4604 | 100 | 0-65535 | Key 82 Retro Time(ms) |
| 4605 | 0 | 0-30000 | Key 82 Max On Time(ms) |
| 4650 | 65 | 0-376 | Key 83 On Force |
| 4651 | 0 | 0-255 | Key 83 Force Curve ID |
| 4652 | 376 | 0-376 | Key 83 Max Force |
| 4653 | 3 | 1-255 | Key 83 Retro Divisor |
| 4654 | 100 | 0-65535 | Key 83 Retro Time(ms) |
| 4655 | 0 | 0-30000 | Key 83 Max On Time(ms) |
| 4700 | 65 | 0-376 | Key 84 On Force |
| 4701 | 0 | 0-255 | Key 84 Force Curve ID |
| 4702 | 376 | 0-376 | Key 84 Max Force |
| 4703 | 3 | 1-255 | Key 84 Retro Divisor |
| 4704 | 100 | 0-65535 | Key 84 Retro Time(ms) |
| 4705 | 0 | 0-30000 | Key 84 Max On Time(ms) |
| 4750 | 65 | 0-376 | Key 85 On Force |
| 4751 | 0 | 0-255 | Key 85 Force Curve ID |
| 4752 | 376 | 0-376 | Key 85 Max Force |
| 4753 | 3 | 1-255 | Key 85 Retro Divisor |
| 4754 | 100 | 0-65535 | Key 85 Retro Time(ms) |
| 4755 | 0 | 0-30000 | Key 85 Max On Time(ms) |
| 4800 | 65 | 0-376 | Key 86 On Force |
| 4801 | 0 | 0-255 | Key 86 Force Curve ID |
| 4802 | 376 | 0-376 | Key 86 Max Force |
| 4803 | 3 | 1-255 | Key 86 Retro Divisor |
| 4804 | 100 | 0-65535 | Key 86 Retro Time(ms) |
| 4805 | 0 | 0-30000 | Key 86 Max On Time(ms) |
| 4850 | 65 | 0-376 | Key 87 On Force |
| 4851 | 0 | 0-255 | Key 87 Force Curve ID |
| 4852 | 376 | 0-376 | Key 87 Max Force |
| 4853 | 3 | 1-255 | Key 87 Retro Divisor |
| 4854 | 100 | 0-65535 | Key 87 Retro Time(ms) |
| 4855 | 0 | 0-30000 | Key 87 Max On Time(ms) |
| 4900 | 65 | 0-376 | Key 88 On Force |
| 4901 | 0 | 0-255 | Key 88 Force Curve ID |
| 4902 | 376 | 0-376 | Key 88 Max Force |
| 4903 | 3 | 1-255 | Key 88 Retro Divisor |
| 4904 | 100 | 0-65535 | Key 88 Retro Time(ms) |
| 4905 | 0 | 0-30000 | Key 88 Max On Time(ms) |
| 4950 | 65 | 0-376 | Key 89 On Force |
| 4951 | 0 | 0-255 | Key 89 Force Curve ID |
| 4952 | 376 | 0-376 | Key 89 Max Force |
| 4953 | 3 | 1-255 | Key 89 Retro Divisor |
| 4954 | 100 | 0-65535 | Key 89 Retro Time(ms) |
| 4955 | 0 | 0-30000 | Key 89 Max On Time(ms) |
| 5000 | 65 | 0-376 | Key 90 On Force |
| 5001 | 0 | 0-255 | Key 90 Force Curve ID |
| 5002 | 376 | 0-376 | Key 90 Max Force |
| 5003 | 3 | 1-255 | Key 90 Retro Divisor |
| 5004 | 100 | 0-65535 | Key 90 Retro Time(ms) |
| 5005 | 0 | 0-30000 | Key 90 Max On Time(ms) |
| 5050 | 65 | 0-376 | Key 91 On Force |
| 5051 | 0 | 0-255 | Key 91 Force Curve ID |
| 5052 | 376 | 0-376 | Key 91 Max Force |
| 5053 | 3 | 1-255 | Key 91 Retro Divisor |
| 5054 | 100 | 0-65535 | Key 91 Retro Time(ms) |
| 5055 | 0 | 0-30000 | Key 91 Max On Time(ms) |
| 5100 | 65 | 0-376 | Key 92 On Force |
| 5101 | 0 | 0-255 | Key 92 Force Curve ID |
| 5102 | 376 | 0-376 | Key 92 Max Force |
| 5103 | 3 | 1-255 | Key 92 Retro Divisor |
| 5104 | 100 | 0-65535 | Key 92 Retro Time(ms) |
| 5105 | 0 | 0-30000 | Key 92 Max On Time(ms) |
| 5150 | 65 | 0-376 | Key 93 On Force |
| 5151 | 0 | 0-255 | Key 93 Force Curve ID |
| 5152 | 376 | 0-376 | Key 93 Max Force |
| 5153 | 3 | 1-255 | Key 93 Retro Divisor |
| 5154 | 100 | 0-65535 | Key 93 Retro Time(ms) |
| 5155 | 0 | 0-30000 | Key 93 Max On Time(ms) |
| 5200 | 65 | 0-376 | Key 94 On Force |
| 5201 | 0 | 0-255 | Key 94 Force Curve ID |
| 5202 | 376 | 0-376 | Key 94 Max Force |
| 5203 | 3 | 1-255 | Key 94 Retro Divisor |
| 5204 | 100 | 0-65535 | Key 94 Retro Time(ms) |
| 5205 | 0 | 0-30000 | Key 94 Max On Time(ms) |
| 5250 | 65 | 0-376 | Key 95 On Force |
| 5251 | 0 | 0-255 | Key 95 Force Curve ID |
| 5252 | 376 | 0-376 | Key 95 Max Force |
| 5253 | 3 | 1-255 | Key 95 Retro Divisor |
| 5254 | 100 | 0-65535 | Key 95 Retro Time(ms) |
| 5255 | 0 | 0-30000 | Key 95 Max On Time(ms) |
| 5515 | 0 | 0-1 | Remote Support Enable |
| 10000 | 0 |  | Tempo |
| 10002 | 0 |  | Transpose |
| 10001 | 0 |  | Tempo Persist |
| 10003 | 0 |  | Transpose Persist |
| -1 | None |  |  |
