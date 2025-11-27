import os
import uuid
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()


class StoryGenerator:
    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.8,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # vector store 
        self.vector_store = self._initialize_vector_store()
        
        # เก็บ story
        self.sessions: Dict[str, Dict] = {}
        
        # สร้างเรื่อง
        self.story_template = PromptTemplate(
            input_variables=["theme", "context", "reference_stories", "inventory"],
            template="""คุณเป็น AI นักเขียนเรื่องราวแบบ text adventure game ที่มีความสามารถสูงและเข้มงวดเรื่องความสมเหตุสมผล

ธีม: {theme}
บริบทเรื่อง: {context}
สิ่งของในกระเป๋า: {inventory}

อ้างอิงจากเรื่องราวที่คล้ายกัน:
{reference_stories}

**กฎสำคัญ**:
1. ตรวจสอบว่าผู้เล่นมีสิ่งของที่ต้องการใช้ในกระเป๋าหรือไม่
2. ถ้าผู้เล่นพยายามใช้สิ่งที่ไม่มีในกระเป๋า ให้บอกว่า "คุณไม่มี[สิ่งนั้น]ในกระเป๋า"
3. เมื่อผู้เล่นเก็บของ ให้เพิ่มเข้าไปใน INVENTORY
4. เมื่อผู้เล่นใช้หรือทิ้งของ ให้ลบออกจาก INVENTORY
5. ตรวจสอบว่าการกระทำสมเหตุสมผลตามธีมและสถานการณ์
6. การกระทำบางอย่างอาจนำไปสู่อันตราย ความตาย หรือจุดจบทันที

สร้างเนื้อเรื่องสั้นๆ (3-5 ประโยค) ที่น่าสนใจและเหมาะกับธีม

รูปแบบการตอบกลับ:
NARRATIVE: [เนื้อเรื่อง - ถ้าการกระทำไม่สมเหตุสมผลให้บอกว่า "ที่นี่ไม่มี..." หรือ "คุณไม่มี...ในกระเป๋า"]
DIRECTIONS: [ทิศทางที่ไปได้ เช่น "หน้า, ซ้าย, ขวา" - ถ้าเรื่องจบให้เว้นว่าง]
OBJECTS: [สิ่งของที่สำรวจได้ เช่น "ประตูไม้, หีับสมบัติ" - ถ้าเรื่องจบให้เว้นว่าง]
HINT: [คำแนะนำสั้นๆ - ถ้าเรื่องจบให้เว้นว่าง]
INVENTORY: [รายการสิ่งของในกระเป๋าปัจจุบัน เช่น "ดาบ, คบเพลิง, กุญแจ" - ถ้าไม่มีให้ใส่ "ไม่มี"]

ตอบเป็นภาษาไทยเท่านั้น"""
        )
    
    def _initialize_vector_store(self):
        # Story templates 
        story_templates = [
            "ผจญภัย: คุณตื่นขึ้นมาในป่าลึก มีแผนที่ปริศนาในมือ คุณได้ยินเสียงแปลกๆ จากด้านหลัง",
            "ผจญภัย: คุณเป็นนักผจญภัยที่กำลังมองหาสมบัติในถ้ำโบราณ แสงไฟฉายส่องไปเห็นประตูสามบาน",
            "ลึกลับ: ในคฤหาสน์เก่าแก่ คุณพบจดหมายลึกลับที่เขียนเมื่อ 50 ปีก่อน มีเสียงฝีเท้าดังขึ้นชั้นบน",
            "ลึกลับ: คุณเป็นนักสืบที่ได้รับมอบหมายคดีปริศนา มีพยานสามคนให้การขัดแย้งกัน",
            "ไซไฟ: คุณตื่นขึ้นในยานอวกาศ ลูกเรือคนอื่นหายตัวไปหมด เครื่องมือตรวจจับแสดงสัญญาณชีวิตแปลกปลอม",
            "ไซไฟ: ในโลกอนาคต AI ครองโลก คุณเป็นหนึ่งในมนุษย์ที่เหลือรอด ต้องเลือกระหว่างสู้หรือร่วมมือ",
            "สยองขวัญ: กลางดึกในบ้านเก่า คุณได้ยินเสียงเด็กหัวเราะ แต่คุณอยู่คนเดียว กระจกเริ่มเป็นฝ้า",
            "สยองขวัญ: คุณเข้าไปในโรงพยาบาลร้าง หาเพื่อนที่หายไป เสียงรถเข็นดังจากระเบียงที่มืดมิด",
            "โรแมนติก: คุณพบจดหมายรักจากคนรู้จัก มีการนัดพบที่ร้านกาแฟ แต่มีคนสองคนปรากฏตัว",
            "โรแมนติก: ในงานเลี้ยงรุ่น คุณเจอรักเก่าที่เคยจากกันไป ความรู้สึกเดิมๆ กลับมาอีกครั้ง",
            "แฟนตาซี: คุณเป็นพ่อมดฝึกหัดที่เพิ่งค้นพบคาถาโบราณ ต้องเลือกระหว่างใช้มันเพื่อช่วยโลกหรือทำลายศัตรู",
            "แฟนตาซี: ในอาณาจักรเวทมนตร์ คุณได้รับภารกิจสำคัญในการค้นหาหินวิเศษที่ถูกขโมยไป",
            "ดราม่า: คุณเป็นนักแสดงที่กำลังเผชิญหน้ากับวิกฤตในชีวิตส่วนตัวและอาชีพการงาน",
            "ดราม่า: ในครอบครัวที่มีความลับมากมาย คุณต้องตัดสินใจว่าจะเปิดเผยความจริงหรือเก็บมันไว้"
        ]
        
        # vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50
        )
        
        texts = text_splitter.create_documents(story_templates)
        vector_store = FAISS.from_documents(texts, self.embeddings)
        
        return vector_store
    
    def _get_relevant_stories(self, theme: str, k: int = 2) -> str:

        docs = self.vector_store.similarity_search(theme, k=k)
        return "\n".join([doc.page_content for doc in docs])
    
    def _parse_response(self, response: str) -> Dict:
        """แปลงผลลัพธ์จาก LLM"""
        lines = response.strip().split("\n")
        result = {
            "narrative": "",
            "directions": [],
            "objects": [],
            "hint": "",
            "inventory": [],
            "is_ending": False
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith("NARRATIVE:"):
                result["narrative"] = line.replace("NARRATIVE:", "").strip()
            elif line.startswith("DIRECTIONS:"):
                directions_text = line.replace("DIRECTIONS:", "").strip()
                # แยกทิศทางด้วย comma
                result["directions"] = [d.strip() for d in directions_text.split(",") if d.strip()]
            elif line.startswith("OBJECTS:"):
                objects_text = line.replace("OBJECTS:", "").strip()
                # แยกสิ่งของด้วย comma
                result["objects"] = [o.strip() for o in objects_text.split(",") if o.strip()]
            elif line.startswith("HINT:"):
                result["hint"] = line.replace("HINT:", "").strip()
            elif line.startswith("INVENTORY:"):
                inventory_text = line.replace("INVENTORY:", "").strip()
                # แยกสิ่งของในกระเป๋าด้วย comma
                if inventory_text and inventory_text.lower() != "ไม่มี":
                    result["inventory"] = [i.strip() for i in inventory_text.split(",") if i.strip()]
    
        
        return result
    
    async def start_story(self, theme: str) -> Dict:
        """เริ่มเรื่องราวใหม่"""
        story_id = str(uuid.uuid4())

        reference_stories = self._get_relevant_stories(theme)

        #เรื่องเริ่มต้น
        context = "เริ่มต้นเรื่องราว - แนะนำที่มาที่ไปของตัวละครหลัก ว่ามาจากไหน มาที่นี่ทำไม มีจุดประสงค์อะไร และอยู่ในสถานการณ์แบบไหน บอกสิ่งของเริ่มต้นที่มีติดตัว"
        chain = self.story_template | self.llm
        response = await chain.ainvoke({
            "theme": theme,
            "context": context,
            "reference_stories": reference_stories,
            "inventory": "ไม่มี"
        })
        
        parsed = self._parse_response(response.content)
        
        # บันทึก session
        self.sessions[story_id] = {
            "theme": theme,
            "history": [context, parsed["narrative"]],
            "turn": 1,
            "current_location": parsed["narrative"],
            "inventory": parsed.get("inventory", []) 
        }
        
        print(f"[Story {story_id[:8]}] Turn 1 - เริ่มเรื่อง: {theme}")
        
        return {
            "story_id": story_id,
            "narrative": parsed["narrative"],
            "directions": parsed.get("directions", []),
            "objects": parsed.get("objects", []),
            "hint": parsed.get("hint", ""),
            "inventory": parsed.get("inventory", []),
            "is_ending": parsed["is_ending"]
        }
    
    async def continue_story(self, story_id: str, user_action: str) -> Dict:
        """ดำเนินเรื่องต่อตามการกระทำของผู้เล่น"""
        if story_id not in self.sessions:
            raise ValueError("Story session not found")
        
        session = self.sessions[story_id]
        session["turn"] += 1
        
        print(f"[Story {story_id[:8]}] Turn {session['turn']} - ผู้เล่น: {user_action}")
        
        history_context = " ".join(session["history"][-3:])
        full_context = f"{history_context}\nผู้เล่น: {user_action}"
        

        reference_stories = self._get_relevant_stories(session["theme"])
        
        current_inventory = session.get("inventory", [])
        inventory_text = ", ".join(current_inventory) if current_inventory else "ไม่มี"
        
        # turn สูงสุด
        if session["turn"] >= 15:
            print(f"[Story {story_id[:8]}] Turn {session['turn']} - ถึง turn สูงสุด! กำลังสร้างฉากจบ...")
            full_context += "\n[นี่คือตอนจบของเรื่อง! สร้างฉากจบที่สมบูรณ์ อธิบายให้ชัดเจนว่า:\n1. เกิดอะไรขึ้นกับตัวละครหลักหลังจากการกระทำนี้\n2. ตัวละครหลักมีชีวิตรอดหรือไม่ ถ้าตายให้บอกว่าตายอย่างไร ถ้ารอดให้บอกว่ารอดอย่างไรและมีชีวิตต่อไปอย่างไร\n3. ผลที่ตามมาจากการตัดสินใจทั้งหมด\n4. บทสรุปของเรื่องราวทั้งหมด\nเขียนเป็นเรื่องราวที่ยาวและละเอียด 5-8 ประโยค\nไม่ต้องระบุ DIRECTIONS, OBJECTS, HINT]"
        
        chain = self.story_template | self.llm
        response = await chain.ainvoke({
            "theme": session["theme"],
            "context": full_context,
            "reference_stories": reference_stories,
            "inventory": inventory_text
        })
        
        parsed = self._parse_response(response.content)
        
        if "inventory" in parsed and parsed["inventory"]:
            session["inventory"] = parsed["inventory"]
        
  
        session["history"].append(user_action)
        session["history"].append(parsed["narrative"])
        
      
        
        is_ending = session["turn"] >= 15 or self._check_if_ending(parsed["narrative"])
        
        # ถ้าจบ
        if is_ending:
            print(f"[Story {story_id[:8]}] เรื่องจบแล้ว! (Turn: {session['turn']})")
        
        return {
            "story_id": story_id,
            "narrative": parsed["narrative"],
            "directions": parsed.get("directions", []) if not is_ending else [],
            "objects": parsed.get("objects", []) if not is_ending else [],
            "hint": parsed.get("hint", "") if not is_ending else "",
            "inventory": session.get("inventory", []),
            "is_ending": is_ending
        }
    
    def _check_if_ending(self, narrative: str) -> bool:
        """ตรวจสอบว่าเนื้อเรื่องเป็นตอนจบหรือไม่"""
        # คำสำคัญที่บ่งชี้ฉากจบชัดเจน
        strong_ending_keywords = [
            "ตายแล้ว", "เสียชีวิตแล้ว", "สิ้นใจแล้ว", "หมดลมหายใจ",
            "จบเรื่อง", "จบลง", "จบเกม",
            "ชัยชนะครั้งยิ่งใหญ่", "ประสบความสำเร็จในที่สุด",
            "พ่ายแพ้อย่างราบคาบ", "ล้มเหลวอย่างสิ้นเชิง",
            "รอดชีวิตมาได้", "หนีออกมาได้สำเร็จ", "หลบหนีออกมาได้",
            "ถูกจับได้", "ติดกับดักแล้ว", "ไม่มีทางออกอีกต่อไป",
            "ยอมแพ้", "ยอมจำนน", "ยอมจนน", "ยอมพ่ายแพ้",
            "หนีกลับบ้าน", "หนีกลับ", "วิ่งหนี", "ถอยหนี", "หนีไป",
            "ล้มเลิก", "เลิกเล่น", "ไม่เล่นแล้ว", "เลิกทำ"
        ]
        
        narrative_lower = narrative.lower()
    
        for keyword in strong_ending_keywords:
            if keyword in narrative_lower:
                return True
        
        return False
