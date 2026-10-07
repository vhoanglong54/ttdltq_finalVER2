# Geographic Map asset and audit

`oulad_regions.geojson` là geometry **xấp xỉ có kiểm soát** cho 13 nhãn `region` của OULAD. Đây không phải bộ polygon chính thức do Open University phát hành.

## Nguồn và giấy phép

- Geometry gốc: Office for National Statistics, *Counties and Unitary Authorities (December 2025) Boundaries UK BGC*.
- Trang nguồn: <https://www.data.gov.uk/dataset/563f5079-796d-4190-ac7f-49219a6de896/counties-and-unitary-authorities-december-2025-boundaries-uk-bgc>
- Dịch vụ dữ liệu: ONS Open Geography ArcGIS Feature Service.
- Giấy phép: Open Government Licence v3.0.
- Mô tả vùng lịch sử: [The Open University, healthcare practice qualifications prospectus (2015)](https://css2.open.ac.uk/outis/docs/publications/NAH16U.pdf), mục regional/national centres và “Area covered”.

## Cách dựng

```powershell
python src/build_oulad_regions_geojson.py
```

Script tải các Counties/Unitary Authorities chính thức, ánh xạ từng đơn vị vào vùng OU lịch sử, union polygon, đơn giản hóa 0,005 độ để dùng trên dashboard, rồi kiểm tra nhãn OULAD đủ 13/13. `oulad_regions_mapping.csv` là bảng audit từng đơn vị ONS.

## Quyết định và giới hạn

- `Ireland` được biểu diễn bằng **Northern Ireland như một proxy**, vì nguồn geometry ONS chỉ bao phủ UK, văn phòng OU được đặt tại Belfast, còn OULAD chỉ cung cấp nhãn rộng `Ireland`. Không suy diễn polygon này bao phủ chính xác mọi học viên mang nhãn Ireland.
- Channel Islands và Isle of Man được nêu trong mô tả OU cũ nhưng không nằm trong bộ ranh giới hành chính UK của ONS, nên không xuất hiện trong polygon.
- Một số vùng lịch sử chia nhỏ county cũ (một phần Wiltshire, Staffordshire hoặc Derbyshire). Bộ ONS hiện tại ở hạt Counties/Unitary Authorities không tái hiện chính xác đường chia đó. Quy ước hiện tại là: Wiltshire → South West; Swindon → South; Staffordshire → West Midlands; Derbyshire → East Midlands.
- North/North East Lincolnshire được đặt vào East Midlands; Kingston upon Hull và East Riding được đặt vào Yorkshire.
- Geometry này phù hợp để biểu diễn **phân bố không gian khái quát** của rate theo nhãn OULAD, không phù hợp cho phân tích ranh giới hành chính chi tiết hoặc suy luận cá nhân.
- Bar chart theo region luôn được giữ cạnh map để kiểm tra rate, `N` và tránh diễn giải sai do diện tích polygon.

Map chỉ được nghiệm thu khi `oulad_regions.geojson` có 13 feature, mọi `properties.region` khớp dữ liệu, tổng `N` khớp filter context và tooltip hiển thị attempts/At-Risk count/rate.
