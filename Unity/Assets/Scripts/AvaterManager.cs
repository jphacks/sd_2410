using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvaterManager : MonoBehaviour
{
    AudioSource _audioSource;
    public AudioClip _audioClip;
    [SerializeField] private Animation[] _animation;
    [SerializeField] private GameObject _gameObject;

    void Start()
    {
        _audioSource = GetComponent<AudioSource>();
    }

    // ChatGPT���特���e�L�X�g���擾
    public void GetAudioText()
    {
        //_audioClip = () ���
    }

    // �����ƃA�j���[�V�����̍Đ�
    public void PlayAnimation()
    {
        //if ()
        //{

        //}

        _audioSource.PlayOneShot(_audioClip);
    }
}
