# System Monitor

โปรเจค System Monitor App ได้รับแรงบรรดาลใจจากการมาถึงของ AI ที่หลากหลาย รวมถึงโมเดลการพัฒนา AI ที่มีมากมาย ไม่ว่าจะเป็น Clustering , Natural Language , Neural Network เป็นต้น แต่การที่เราจะพัฒนา AI ผ่านโมเดลมากมายเหล่านี้ได้
เราจะเป็นต้องมี ทรัพยากรทางคอมพิวเตอร์ที่สูงพอสมควร จึงเป็นที่มาของโปรเจคนี้ system monitor ถูกพัฒนาขึ้นเพื่อ ทดสอบคอมพิวเตอร์หรือโน้ตบุ๊คของผู้ใช้ ว่ามีประสิทธิภาพสูงพอที่จะสามารถประมวลผลด้านโมเดล AI ต่างๆได้มีประสิทธิภาพอย่างไร

# รูปแบบการทำงาน
โดยsystem monitor จะแบ่งการทดสอบเป็น 4 แบบ คือ
1. single core นั้นคือ การใช้คอลเดี่ยว ทำทีละงาน
2. multi core นั้นคือ การใช้คอลคู่ ทำทีละงาน
3. threaded core นั้นคือ การใช้คอลเดี่ยว ทำงานพร้อมกันหลายงาน
4. multiprocessir core นั้นคือ การใช้คอลคู่ ทำงานพร้อมกันหลายงาน

# โมเดลที่นำมาใช้ในการทดสอบ
ซึ่งเราคงมีคำถามว่า งานที่ว่าคืออะไร งานในที่นี่คือ โมเดลรูปแบบต่างๆที่เรานำมาใช้ทดสอบคอมพิวเตอร์ ประกอบด้วย
1. Neural Network ->	simulate_neural_network ->	MLPClassifier ->	โครงข่ายประสาทเทียมพื้นฐาน
2. Image Recognition ->	simulate_image_recognition ->	MLPClassifier ->	ใช้กับภาพที่ flatten แล้ว
3. Natural Language ->	simulate_natural_language ->	MLPClassifier ->	จำลองข้อความด้วย vector
4. Data Classification ->	simulate_data_classification ->	MLPClassifier ->	วัดความแม่นยำด้วย accuracy
5. Clustering -> simulate_clustering ->	KMeans ->	ไม่มี label ใช้การจัดกลุ่ม

# Dowload System Monitor App
DowloadApp = https://drive.google.com/drive/folders/1zx7ZW2VzMThAmwDMC8A41NCT0kHla6wb?usp=sharing

1. ดาวโหลดผ่าน link ด้านบน กด dowload ผ่านdriveของท่าน ท่านจะได้รับ zip file เป็น system monitor2
2. เมื่อแตกไฟล์ กดคลิกเข้าไปจะพบ folder dist กดเข้าไปอีกครั้ง จะพบ system-monitor.exe
3. เมื่อดับเบิ้ลคลิกที่ไฟล์ โปรดรอสักครู่ จะมีโปรแกรมแสดงออกมา
4. กดเลือก tab Ai test ด้านบน ท่าจะพบหน้าทดสอบ AI
5. ส่วนแรก คือ Device ท่านสามารถเลือกได้ว่าจะทดสอบด้วย CPU หรือ GPU
6. ส่วนที่สอง คือ Mode ประกอบด้วย single multi threaded multiprocessir (คำอธิบายอยู่ที่หัวข้อ รูปแบบการทำงาน)
7. ส่วนที่สาม คือ start ai เราจะต้องทำการเลือกโหมดในการทดสอบ แล้วจึงกด start เมื่อทดสอบสำเร็จโปรแกรม จะแสดงกราฟออกมา โดยประกอบด้วย 5 กราฟแทน 5 โมเดลAI และ เวลาที่ใช้และคะแนนที่ได้
8. ส่วนที่สี่ คือ compare คือ การทดสอบทั้ง 4 รูปแบบการทำงานพร้อมกัน แต่จะไล่ระดับจาก single ไปหา multiprocessir ซึ่งจะแสดงกราฟออกมาปกติ แต่จะแสดงทั้ง 4 รูปแบบ ตามด้วยเส้นกราฟที่จะโชว์ว่า รูปแบบการทำงานไหนที่โดดเด่นในการทดสอบ

# ความรู้เบื้องต้นเกี่ยวกับ โมเดลที่ใช้ในการทดสอบ
1. Clustering (การจัดกลุ่มข้อมูล) คือกระบวนการจัดกลุ่ม (cluster) ของข้อมูลที่คล้ายกันเข้าไว้ด้วยกัน โดยข้อมูลที่อยู่ในกลุ่มเดียวกันจะมีความคล้ายคลึงกันมากกว่าข้อมูลในกลุ่มอื่น

    กระบวนการของ Clustering โดยทั่วไป:
   
    > เตรียมข้อมูล (Preprocessing) ล้างข้อมูล, แปลงข้อมูลเป็นตัวเลข (ถ้าเป็นข้อความ)

    > เลือกจำนวนกลุ่ม (k) บางเทคนิคต้องกำหนดจำนวนกลุ่ม เช่น K-Means ต้องกำหนด k

    > คำนวณความใกล้เคียง (Similarity/Distance) ใช้สูตรเช่น Euclidean distance หรือ Cosine similarity

    > แบ่งกลุ่มข้อมูล (Assign Clusters) โมเดลจะจับกลุ่มข้อมูลที่มีลักษณะคล้ายกัน

    > วิเคราะห์ผลลัพธ์ ดูว่าการจัดกลุ่มมีประโยชน์หรือไม่? สามารถนำไปใช้งานต่อได้ไหม?

2. Data Classification คือกระบวนการที่โมเดลเรียนรู้จากชุดข้อมูลที่ “มีป้ายกำกับ” (Label) เพื่อทำนายประเภทของข้อมูลใหม่ที่ยังไม่รู้ว่าคืออะไร

   ขั้นตอนของ Classification:

   > รวบรวมข้อมูล (Data Collection) ต้องมีทั้ง Feature และ Label

   > เตรียมข้อมูล (Preprocessing) แปลงข้อความเป็นตัวเลข, จัดการค่าหาย, Normalization

   > แยกข้อมูลเป็น Train/Test เช่น 80% ฝึก (Training), 20% ทดสอบ (Testing)

   > เลือกโมเดล Classification เช่น Decision Tree, Logistic Regression, SVM, KNN, Neural Network

   > ฝึกโมเดล (Train) โมเดลเรียนรู้จากชุด Train

   > ทดสอบโมเดล (Evaluate) ใช้ข้อมูล test ดูว่าโมเดลทำนายถูกหรือไม่

   > ใช้งานจริง (Predict) นำข้อมูลใหม่มาทำนายผล

3. Image Recognition (การรู้จำภาพ) คือ คือกระบวนการที่ให้คอมพิวเตอร์ “รู้จำ” หรือ “เข้าใจ” สิ่งที่อยู่ในรูปภาพ เช่น วัตถุ, บุคคล, สถานที่, หรือข้อความ
โดยอาศัยเทคนิคทาง Machine Learning, Deep Learning โดยเฉพาะ Convolutional Neural Networks (CNN)

  ขั้นตอนของ Image Recognition โดยทั่วไป:
  
  > เก็บข้อมูลภาพ (Image Dataset) เช่น รูปภาพแมว, หมา, รถ ฯลฯ

  > เตรียมข้อมูล (Preprocessing) ปรับขนาดภาพ (resize), ทำ grayscale, normalize ค่า pixel ให้อยู่ระหว่าง 0-1

  > Label ภาพ (Annotation) ต้องรู้ว่าแต่ละภาพคืออะไร เช่น "cat", "dog", "car"

  > สร้างโมเดล CNN (หรือเลือกโมเดลที่ฝึกไว้แล้ว) เช่น ResNet, MobileNet, VGG

  > ฝึกโมเดล (Train) ใช้ภาพและ label เพื่อให้โมเดลเรียนรู้

  > ประเมินผล (Evaluate) ตรวจว่าโมเดลแม่นแค่ไหนในการทำนายภาพใหม่

  > นำไปใช้ (Deploy) บนเว็บ, แอปมือถือ, กล้อง, ฯลฯ
  
4. Natural Language Processing (NLP) คือการทำให้คอมพิวเตอร์สามารถ “เข้าใจ”, “ประมวลผล”, “แปลความหมาย”, และ “สร้าง” ภาษาแบบที่มนุษย์ใช้จริงได้
โดยใช้ทั้งภาษาพูดและภาษาเขียน เช่น การสนทนา, อีเมล, ข่าว, หรือข้อความในโซเชียลมีเดีย

  ขั้นตอนหลักของ NLP:

  > Tokenization – ตัดคำ เช่น “ฉันรักเธอ” → ["ฉัน", "รัก", "เธอ"]

  > Part-of-Speech Tagging – หาว่าคำนั้นเป็น กริยา / คำนาม / คุณศัพท์ ฯลฯ

  > Named Entity Recognition (NER) – แยกชื่อคน, สถานที่, บริษัท ฯลฯ

  > Lemmatization / Stemming – ตัดคำให้อยู่ในรูปพื้นฐาน เช่น “running” → “run”

  > Parsing / Syntax Tree – วิเคราะห์โครงสร้างประโยค

  > Sentiment Analysis – วิเคราะห์ว่าข้อความสื่อถึงอารมณ์อะไร

  > Text Classification – จัดประเภทของข้อความ เช่น ข่าวกีฬา ข่าวการเมือง

  > Machine Translation – แปลภาษาอัตโนมัติ

5. Neural Network (โครงข่ายประสาทเทียม) คือโมเดลคอมพิวเตอร์ที่ได้รับแรงบันดาลใจจากการทำงานของสมองมนุษย์
มีโครงสร้างประกอบด้วย “ชั้นของหน่วยประมวลผล (neurons)” ที่เชื่อมโยงกัน และใช้ในการ “เรียนรู้” จากข้อมูล

  โครงสร้างของ Neural Network
  
  > Input Layer: รับข้อมูลเข้าจากภายนอก เช่น ตัวเลข, รูปภาพ, ข้อความ

  > Hidden Layer(s): เป็นชั้นซ่อน ที่ใช้คำนวณ/เรียนรู้ความสัมพันธ์ของข้อมูล ยิ่งมีหลายชั้น → เรียกว่า Deep Neural Network

  > Output Layer: ให้ผลลัพธ์สุดท้าย เช่น คำตอบว่า "หมา" หรือ "แมว"
  
  > แต่ละชั้นประกอบด้วย “Neurons” (หน่วยย่อยคล้ายเซลล์ประสาท) ซึ่งเชื่อมกันด้วย "น้ำหนัก" (Weights)

# Tool
1. PYTHON (scikit-learn,make_classification,numpy,matplotlib,pandas)
2. FLASK (Restfull-api,connect MongoDB)
3. render.com (Web Service , Static Site)
