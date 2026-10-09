# Morse Hand App

Ứng dụng Python giúp nhập văn bản bằng mã Morse thông qua cử chỉ bàn tay trước webcam. Chương trình sử dụng MediaPipe để nhận diện bàn tay và OpenCV để hiển thị hình ảnh, hướng dẫn thao tác và nội dung đã giải mã.

Ứng dụng hỗ trợ chữ cái **A–Z**, chữ số **0–9** và dấu cách. Đây là ứng dụng tương tác bằng webcam, không có cơ chế tính điểm hay màn chơi.

## 1. Yêu cầu cài đặt

- Sử dụng **Python 3.12** để phù hợp với phiên bản MediaPipe được cố định trong dự án. `pyproject.toml` khai báo Python từ 3.12 trở lên, nhưng khả năng cài đặt trên phiên bản mới hơn còn phụ thuộc thư viện.
- Máy tính có webcam và môi trường đồ họa để mở cửa sổ ứng dụng.
- Cho phép terminal hoặc IDE truy cập camera nếu hệ điều hành yêu cầu.
- Có kết nối Internet khi tải các thư viện lần đầu.

Các thư viện chính theo `pyproject.toml`:

| Thư viện | Phiên bản | Vai trò |
| --- | --- | --- |
| MediaPipe | `0.10.14` | Nhận diện và theo dõi bàn tay |
| OpenCV (`opencv-python`) | `>=5.0.0.93` | Đọc webcam và hiển thị giao diện |

## 2. Cài đặt

Mở terminal tại thư mục dự án `morse_project`, sau đó chọn **một** trong hai cách dưới đây.

### Cách 1: Dùng uv

Nếu máy đã cài `uv`, chạy:

```bash
uv sync --python 3.12 --locked
```

Lệnh này tạo môi trường ảo `.venv` và cài các thư viện theo `uv.lock`.

### Cách 2: Dùng pip và môi trường ảo

**Linux/macOS:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "mediapipe==0.10.14" "opencv-python>=5.0.0.93"
```

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install "mediapipe==0.10.14" "opencv-python>=5.0.0.93"
```

Nếu PowerShell chặn kích hoạt môi trường ảo, có thể dùng trực tiếp Python trong môi trường đó để cài thư viện:

```powershell
.\.venv\Scripts\python.exe -m pip install "mediapipe==0.10.14" "opencv-python>=5.0.0.93"
```

## 3. Chạy chương trình

Nếu cài bằng `uv`:

```bash
uv run --locked python morse_hand.py
```

Nếu cài bằng `pip`, kích hoạt môi trường ảo rồi chạy:

```bash
python morse_hand.py
```

Trên Windows, có thể chạy trực tiếp mà không kích hoạt môi trường ảo:

```powershell
.\.venv\Scripts\python.exe morse_hand.py
```

Chương trình sử dụng camera mặc định có chỉ số `0` và mở cửa sổ **Morse Hand App**. Nhấp vào cửa sổ rồi nhấn **`q`** để thoát và giải phóng camera.

## 4. Hướng dẫn sử dụng

### Giao diện

- **Góc trên bên trái:** hướng dẫn thao tác cho từng ngón tay.
- **MORSE CHART:** bảng tra mã Morse ở góc trên bên phải; ký tự có mã trùng với chuỗi đang nhập được làm sáng.
- **CURRENT LETTER:** chuỗi dấu chấm và gạch ngang đang nhập cho một ký tự.
- **MESSAGE:** văn bản đã được giải mã và xác nhận.

### Điều khiển bằng bàn tay

Đưa một bàn tay vào khung hình, giữ rõ các đầu ngón tay. Dùng **đầu ngón cái** chạm vào đầu ngón tương ứng:

| Thao tác | Chức năng |
| --- | --- |
| Chạm ngón trỏ | Thêm dấu chấm `.` |
| Chạm ngón giữa | Thêm dấu gạch ngang `-` |
| Chạm ngón áp út một lần | Xác nhận chuỗi Morse hiện tại và thêm ký tự vào `MESSAGE` |
| Chạm ngón áp út hai lần, hai lần chạm cách nhau dưới **0,4 giây** | Thêm dấu cách; lần chạm đầu vẫn xác nhận ký tự đang nhập nếu có |
| Chạm ngón út rồi thả, không giữ quá **1,2 giây** | Xóa dấu Morse cuối cùng; nếu chuỗi Morse trống thì xóa ký tự cuối trong `MESSAGE` |
| Giữ chạm ngón út hơn **1,2 giây** | Xóa toàn bộ chuỗi Morse và văn bản |
| Nhấn phím `q` khi cửa sổ ứng dụng đang được chọn | Thoát chương trình |

**Lưu ý:** Tách các ngón ra sau mỗi lần chạm trước khi thực hiện lần chạm tiếp theo. Giữ nguyên thao tác chạm ngón trỏ hoặc ngón giữa chỉ thêm một dấu. Khi xác nhận hai ký tự liên tiếp, để hai lần chạm ngón áp út cách nhau ít nhất 0,4 giây để tránh tạo dấu cách ngoài ý muốn.

### Ví dụ nhập “SOS”

1. Nhập **S (`...`)**: chạm rồi tách ngón cái và ngón trỏ ba lần. Chạm ngón áp út để xác nhận.
2. Nhập **O (`---`)**: chạm rồi tách ngón cái và ngón giữa ba lần. Chạm ngón áp út để xác nhận.
3. Nhập **S (`...`)** như bước 1, rồi xác nhận.
4. Kiểm tra `MESSAGE` hiển thị **SOS**.

Để bắt đầu từ mới, chạm ngón áp út hai lần liên tiếp dưới 0,4 giây. Nếu muốn vừa xác nhận ký tự cuối vừa thêm dấu cách, thực hiện thao tác này khi chuỗi Morse của ký tự cuối vẫn đang ở `CURRENT LETTER`.

Chuỗi Morse không có trong bảng sẽ được chuyển thành **`?`** khi xác nhận. Ứng dụng chưa hỗ trợ chữ tiếng Việt có dấu hoặc lưu văn bản ra tệp; nội dung sẽ mất khi thoát.

## 5. Xử lý sự cố

| Hiện tượng | Cách xử lý |
| --- | --- |
| Không mở được camera hoặc chương trình thoát ngay | Kiểm tra kết nối webcam, quyền camera và đóng ứng dụng khác đang dùng webcam. Nếu có nhiều camera, thử đổi `cv2.VideoCapture(0)` trong `morse_hand.py` sang chỉ số phù hợp, ví dụ `1`. |
| Không nhận diện được bàn tay | Tăng ánh sáng, đưa toàn bộ bàn tay vào khung hình, giữ các ngón rõ và thao tác từng lần. Chương trình chỉ theo dõi tối đa một bàn tay. |
| Chạm tay nhưng không nhập, hoặc nhập nhầm | Điều chỉnh khoảng cách bàn tay với webcam. Có thể tinh chỉnh `TOUCH_THRESHOLD = 0.05` trong mã nguồn: tăng giá trị giúp nhận chạm dễ hơn; giảm giá trị yêu cầu hai đầu ngón gần nhau hơn. |
| Báo `ModuleNotFoundError` | Chạy bằng `uv run --locked python morse_hand.py` hoặc kiểm tra đã cài thư viện trong đúng môi trường `.venv`. |
| Không cài được MediaPipe | Kiểm tra đang dùng Python 3.12 và xem thông báo lỗi về phiên bản Python, hệ điều hành hoặc kiến trúc máy. |
| Lỗi mở cửa sổ OpenCV | Chạy trên máy có giao diện đồ họa và dùng gói OpenCV có hỗ trợ GUI; ứng dụng cần cửa sổ hiển thị và webcam. |

## 6. Cấu trúc dự án

```text
morse_project/
├── morse_hand.py    # Nhận diện cử chỉ, giải mã Morse và hiển thị giao diện
├── pyproject.toml   # Thông tin dự án và yêu cầu thư viện
├── uv.lock          # Các phiên bản thư viện được khóa cho uv
└── README.md        # Hướng dẫn cài đặt, chạy và sử dụng
```
