from dapodik.base import dataclass


@dataclass
class PesertaDidikBaru:
    sekolah_id: str
    nama_pd: str
    jenis_kelamin: str
    tempat_lahir: str
    tanggal_lahir: str
    nama_ibu_kandung: str
    nisn: str = ""
    nik: str = ""
    tahun_ajaran_id: int = 2020
    jenis_pendaftaran_id: int = 1
    sudah_diproses: int = 0
    berhasil_diproses: int = 0
    peserta_didik_id: str = ""
    pdb_id: str = "Admin.model.PesertaDidikBaru-1"
    sekolah_id_str: str = ""
    tahun_ajaran_id_str: str = ""
    jenis_pendaftaran_id_str: str = ""
    peserta_didik_id_str: str = ""
