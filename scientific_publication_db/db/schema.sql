-- ===============================
-- Office
-- ===============================
CREATE TABLE Office (
    OfficeAddress VARCHAR(200) PRIMARY KEY,
    PhoneExtension VARCHAR(20) UNIQUE NOT NULL
);

-- ===============================
-- Researchers
-- ===============================
CREATE TABLE Researchers (
    EmpId INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    OfficeAddress VARCHAR(200),

    FOREIGN KEY (OfficeAddress)
        REFERENCES Office(OfficeAddress)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ===============================
-- Lab Equipment
-- ===============================
CREATE TABLE LabEquipment (
    EquipmentName VARCHAR(100) PRIMARY KEY,
    PrimaryCalibrationStandard VARCHAR(100) NOT NULL
);

-- ===============================
-- Researcher ↔ Lab Equipment (Many-to-Many)
-- ===============================
CREATE TABLE Researcher_Equipment (
    EmpId INT,
    EquipmentName VARCHAR(100),

    PRIMARY KEY (EmpId, EquipmentName),

    FOREIGN KEY (EmpId)
        REFERENCES Researchers(EmpId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (EquipmentName)
        REFERENCES LabEquipment(EquipmentName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ===============================
-- Journal Issue
-- ===============================
CREATE TABLE JournalIssue (
    VolumeIdentifier INT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    PublicationDate DATE NOT NULL,
    Format VARCHAR(50) CHECK (Format IN ('Print', 'Online')),
    EditorInChief INT NOT NULL,

    FOREIGN KEY (EditorInChief)
        REFERENCES Researchers(EmpId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ===============================
-- Research Paper
-- ===============================
CREATE TABLE ResearchPaper (
    PaperId INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200) UNIQUE NOT NULL,
    VolumeIdentifier INT,
    LeadAuthor INT NOT NULL,

    FOREIGN KEY (VolumeIdentifier)
        REFERENCES JournalIssue(VolumeIdentifier)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (LeadAuthor)
        REFERENCES Researchers(EmpId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ===============================
-- Paper ↔ Authors (Many-to-Many)
-- ===============================
CREATE TABLE Paper_Authors (
    PaperId INT,
    EmpId INT,

    PRIMARY KEY (PaperId, EmpId),

    FOREIGN KEY (PaperId)
        REFERENCES ResearchPaper(PaperId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (EmpId)
        REFERENCES Researchers(EmpId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
