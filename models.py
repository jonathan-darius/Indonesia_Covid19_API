from sqlalchemy import Column,String,BigInteger
from database import Base


class Covid_Data(Base):
    __tablename__ = "tb_harian"
    date = Column(String, primary_key=True)
    meninggal = Column(BigInteger)
    sembuh = Column(BigInteger)
    positif = Column(BigInteger)
    dirawat = Column(BigInteger)
    kum_meninggal = Column(BigInteger)
    kum_sembuh = Column(BigInteger)
    kum_positif = Column(BigInteger)
    kum_dirawat = Column(BigInteger)