from ultralytics import SAM

# Load a model
SAM_model = SAM('sam_b.pt')
image_path = 'images/6_0.jpg'
image_name = image_path.split("/")[-1][:-4]
print(image_name)
clas = 50
# Run inference with points prompt
results = SAM_model(image_path, bboxes=[150, 300, 900, 550], show=True)

segments = results[0].masks.xyn
with open(f'labels/{image_name}.txt', 'w') as f:
    for i in range(len(segments)):
        s = segments[i]
        if len(s) == 0:
            continue
        segment = map(str, segments[i].reshape(-1).tolist())
        f.write(f'{clas} ' + ' '.join(segment) + '\n')


# from ultralytics.data.annotator import auto_annotate
#
# auto_annotate(data="images", det_model="yolov8x.pt", sam_model='sam_b.pt')