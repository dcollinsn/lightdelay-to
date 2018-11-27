from django.db import models


class MinorPlanet(models.Model):
    name = models.CharField(max_length=64, unique=True)
    inclination = models.FloatField()
    node = models.FloatField()
    peri = models.FloatField()
    semimajor = models.FloatField()
    motion = models.FloatField()
    eccentricity = models.FloatField()
    anomaly = models.FloatField()
    packed_epoch = models.CharField(max_length=5)
    equinox_year = models.CharField(max_length=4)
    magnitude_model = models.CharField(max_length=16)

    @property
    def epoch_date(self):
        year_major = self.packed_epoch[0:1]
        year_minor = int(self.packed_epoch[1:3])
        month = self.packed_epoch[3:4]
        day = self.packed_epoch[4:5]
        if year_major == 'I':
            year = 1800 + year_minor
        elif year_major == 'J':
            year = 1900 + year_minor
        elif year_major == 'K':
            year = 2000 + year_minor
        else:
            raise NotImplementedError
        unpack_table = {
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
            'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22,
            'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
            'U': 30, 'V': 31,
        }
        return '%02d/%02d/%04d' % (
            unpack_table[month],
            unpack_table[day],
            year,
        )

    @property
    def xephem(self):
        return "%s,e,%.4f,%.4f,%.4f,%.6f,%.7f,%.8f,%.4f,%s,%s,%s" %(
            self.name,
            self.inclination,
            self.node,
            self.peri,
            self.semimajor,
            self.motion,
            self.eccentricity,
            self.anomaly,
            self.epoch_date,
            self.equinox_year,
            self.magnitude_model,
        )

    @classmethod
    def from_mpc(this_class, mpc_row):
        self = this_class()

        desig = mpc_row[0:7].strip()
        H = mpc_row[8:13].strip()
        G = mpc_row[14:19].strip()
        packed_epoch = mpc_row[20:25].strip()
        anomaly = mpc_row[26:35].strip()
        perihelion = mpc_row[37:46].strip()
        node = mpc_row[48:57].strip()
        inclination = mpc_row[59:68].strip()
        eccentricity = mpc_row[70:79].strip()
        motion = mpc_row[80:91].strip()
        semimajor = mpc_row[92:103].strip()
        name = mpc_row[166:194].strip()

        name = name.replace('(', '')
        name = name.replace(')', '')

        self.name = name
        self.inclination = float(inclination)
        self.node = float(node)
        self.peri = float(perihelion)
        self.semimajor = float(semimajor)
        self.motion = float(motion)
        self.eccentricity = float(eccentricity)
        self.anomaly = float(anomaly)
        self.packed_epoch = packed_epoch
        self.equinox_year = '2000'
        self.magnitude_model = 'H%s,%s' % (H, G)
        return self

    def __str__(self):
        return 'Minor Planet %s (#%d)' % (self.name, self.id)
