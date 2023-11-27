# Human Emotion Detection with Electrocardiographic-Electroencephelographic and Other Signals

#### Team

- E/17/144, KPCDB Jayaweera, [e17144@eng.pdn.ac.lk](mailto:e17144@eng.pdn.ac.lk)
- E/17/091, PGAP Gallage, [e17091@eng.pdn.ac.lk](mailto:e17091@eng.pdn.ac.lk)
- E/17/405, WDLP Wijesinghe, [e17405@eng.pdn.ac.lk](mailto:e17405@eng.pdn.ac.lk)

#### Supervisors

- Prof.Roshan Ragel, [roshanr@eng.pdn.ac.lk](mailto:roshanr@eng.pdn.ac.lk)
- Dr.Isuru Nawinne, [isurunawinne@eng.pdn.ac.lk](mailto:isurunawinne@eng.pdn.ac.lk)
- Dr.Mahanama Wickramasinghe, [mahanamaw@eng.pdn.ac.lk](mailto:mahanamaw@eng.pdn.ac.lk)
- Dr.Vajira Thambawita, [vajira@simula.no](mailto:vajira@simula.no)

#### Table of content

1. [Abstract](#abstract)
2. [Related works](#related-works)
3. [Methodology](#methodology)
4. [Experiment Setup and Implementation](#experiment-setup-and-implementation)
5. [Results and Analysis](#results-and-analysis)
6. [Conclusion](#conclusion)
7. [Publications](#publications)
8. [Links](#links)

## Abstract

In this research, we explore the integration of Electroencephalography (EEG) and Electrocardiography (ECG) data to classify human emotions through Convolutional Neural Networks (CNN) to enhance emotion classification accuracy.

Our study involves our own data collection process from participants via video and audio stimuli to elicit five distinct emotions. However, due to the limited sample size, our approach is trained on the DREAMER dataset, which provides signals recorded during affect elicitation via audio-visual stimuli from 23 participants, along with their self-assessment in terms of valence, arousal, and dominance.

Understanding and classifying human emotions is a complex and an important aspect of human-computer interaction and healthcare. EEG captures neural activity and reflects neural patterns associated with cognitive processing, while ECG records cardiac signals and provides insights into autonomic nervous system responses. The combination of these two enhances the robustness and depth of emotion classification and helps to accurately identify emotions of a person at a given instance.

## Related works

The research area of using physiological signals for human emotion detection is an expansive and enduring field, and an infinite number of studies have been done, are going on, and will happen in the future as well. With the advancement of technology, research has also grown to use ML and AI-based techniques in this research area. This section is about the works that are relative to the research. Here you can find a comprehensive Literature review on this field using following link.
- [Comprehensive Review](./docs/public/Pera___emotion_data_collection_survay.pdf)

## Methodology

The project consists of two stages: the data acquisition stage and the development of the CNN model.

#### Stage 1: Data Aquisition

EEG and ECG data were collected during the initial stage of the project. There were several steps to follow for each participant to ensure proper data collection.

1. Read the information sheet
   - Each participant should read the information sheet and get prior knowledge of the study before participating and they must agree to the terms and conditions.
   - [Information Sheet](https://docs.google.com/document/d/1kH4Qc642DGC6JXFG4AZ8_8hR5N0Sukr8RF1XjaJ_s2U/edit)

2. Do the pre experiment survey
   - This is to get the required information about the participant before participating in the study. Note that, all the data that were collected are anonymous and confidential.
   - We are collecting general information (age, gender,..), medical history, background details (nationality, race, religion,..), psychological measures, and technical information which we consider as important to study about the variety of the dataset.
   - [Pre Experiment Survay](https://docs.google.com/forms/d/e/1FAIpQLSewSYhT5gAMh9bNCn5KEJD6RPty2wUojrs8no-RuE5fgjSv6w/viewform)

3. Show audio,video stimuli
   - After completing the pre-experiment survey, we placed the equipment (EEG and ECG electrodes) on the participant and then the videos were shown to the participant.
   - There were five videos considering five emotions.

4. Do the post experiment survey
   - After each video, the relevant section of the post-examination survey was provided to the participants to fill by themself.
   - The reason for this survey was to know to what extent the emotion that we were expecting from the video was stimulated in the participants.
   - [Post Experiment Survay](https://docs.google.com/forms/d/e/1FAIpQLScAYqNibYVf16e_Ot6wFv2-LuvqbFBnrWLDJkyoghvEkMZi2g/viewform)

#### Stage 2: Development of the CNN Model

We have used a CNN base approach to develop the emotion classification model. For experimental stage we have developed two main models;

- Individual CNN model : To classify emotions based on ECG or EEG signal. It uses either one signal to make predictions.
- Combined CNN model : The model was developed to use both EEG & ECG signals together to classify emotions.

The purpose was to identify and compare both individual and compared models according to performance. The model architecture diagrams are shown in the Figure 1 and Figure 2.

<p align="center">
    <img src="./docs/images/single_architecture.png"  width="1000" /><br />
    <span><i>Fig.01: Architecture of the Individual CNN Model</i></span>
</p>

<p align="center">
    <img src="./docs/images/combined_architecture.png"  width="1000" /><br />
    <span><i>Fig.02: Architecture of the Combined CNN Model</i></span>
</p>

## Experiment Setup and Implementation

#### Step 1: Hardware Setup and Data Collection

The hardware setup (EEG device and ECG device) should be correctly placed on the participant before collecting data. It involved several steps;

- There were 8 electrodes in the EEG device. As we used a customized, wearable EEG setup (Fig 03), it was thoroughly checked for correct placement of each electrode on the scalp.
- The ECG device had 3 electrodes and needed to have enough electrode gel before placing them. The electrode placements are shown in Fig 02, 04 and 05.

<p align="center">
    <img src="./docs/images/Experiment_Setup/EEG_Setup.JPG"  width="300" /><br />
    <span><i>Fig.03: EEG Setup</i></span>
</p>

<p align="center">
    <img src="./docs/images/Experiment_Setup/Electrode_Placement_Left.JPG"  width="300" /><br />
    <span><i>Fig.04: Electrode Placement Left</i></span>
</p>

<p align="center">
    <img src="./docs/images/Experiment_Setup/Electrode_Placement_Right.JPG"  width="300" /><br />
    <span><i>Fig.05: Electrode Placement Right</i></span>
</p>

<p align="center">
    <img src="./docs/images/Experiment_Setup/Getting_Data.jpeg"  width="500" /><br />
    <span><i>Fig.06: Data Collection Process</i></span>
</p>

#### Step 2: Software System

The data collection UI was used as the frontend to collect data. There are 5 emotions, therefore 5 videos. After starting the data collection, the video pops into full screen. An image of the UI is shown below.

<p align="center">
    <img src="./docs/images/UI.png"  width="750" /><br />
    <span><i>Data Collection UI</i></span>
</p>

The backend was developed using python flask. As there were 2 process to run parallelly, we added 2 seperate multiprocessors; one for EEG data collection from EEG device and another one for ECG data collection from ECG device.

<p align="center">
    <img src="./docs/images/Multiprocessing.svg"  width="750" /><br />
    <span><i>Backend</i></span>
</p>

#### Step 3: Data and Processing

After collecting data, we have used filters to remove noises that were added from nearby electronic devices.

- Butterworth bandpass filter within the 0.05 Hz to 100 Hz frequency range.
- Frequency of data collection ECG - 1000Hz , EEG - 250Hz

The raw signals and filtered signals are shown in below figures.

<p align="center">
    <img src="./docs/images/ECG_Signals/1.jpeg"  width="750" /><br />
    <span><i>Raw Signal</i></span>
</p>

<p align="center">
    <img src="./docs/images/ECG_Signals/2.jpeg"  width="750" /><br />
    <span><i>Filtered Signal</i></span>
</p>

<p align="center">
    <img src="./docs/images/ECG_Signals/3.jpeg"  width="750" /><br />
    <span><i>Raw Signal - Zoomed</i></span>
</p>

<p align="center">
    <img src="./docs/images/ECG_Signals/4.jpeg"  width="750" /><br />
    <span><i>Filtered Signal - Zoomed</i></span>
</p>

## Results and Analysis

#### Accuracy Comparison with Data Division

| model          | 60 s | 30 s | 20 s | 10 s | 1 s  |
| :------------- | :--- | :--- | :--- | :--- | :--- |
| ECG model      | 50   | 59.1 | 54.7 | 54.7 | 50   |
| EEG model      | 47.6 | 50   | 50   | 47.6 | 47.6 |
| Combined model | 47.6 | 52.6 | 50   | 50   | 47.6 |

<br>

#### ML Model Accuracy Comparison with the DREAMER Research

| model          | This approach | Valence | Arousal | Dominance |
| :------------- | :------------ | :------ | :------ | :-------- |
| ECG model      | 52.4          | 61.8    | 62.3    | 61.8      |
| EEG model      | 59.1          | 62.3    | 62.3    | 61.5      |
| Combined model | 50            | 62.4    | 62.1    | 61.8      |

<!-- ## Conclusion

## Publications -->

## Links

- [Project Repository](https://github.com/cepdnaclk/e17-4yp-Human-Emotion-Detection-with-Electrocardiographic--Electroencephelographic-and-Other-Signals)
- [Project Page](https://cepdnaclk.github.io/e17-4yp-Human-Emotion-Detection-with-Electrocardiographic--Electroencephelographic-and-Other-Signals)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)
- [Download the Research Paper](./public/Pera___emotion_data_collection.pdf)
